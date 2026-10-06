from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import Permission, Role, User
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse
from app.services.audit_service import AuditService
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

def seed_default_roles_and_admin(db: Session):
    permissions_data = [
        ("AUTH_LOGIN", "User Login Permission", "AUTH"),
        ("AUTH_REGISTER", "User Registration Permission", "AUTH"),
        ("USER_CREATE", "Create System User", "USERS"),
        ("USER_READ", "Read System Users", "USERS"),
        ("USER_UPDATE", "Update System User", "USERS"),
        ("USER_DELETE", "Delete System User", "USERS"),
        ("ROLE_CREATE", "Create System Role", "ROLES"),
        ("ROLE_READ", "Read System Roles", "ROLES"),
        ("ROLE_UPDATE", "Update System Role", "ROLES"),
        ("ROLE_DELETE", "Delete System Role", "ROLES"),
        ("inventory.view", "View Inventory", "Inventory"),
        ("inventory.product.create", "Create Product", "Inventory"),
        ("inventory.product.update", "Update Product", "Inventory"),
        ("inventory.product.delete", "Delete Product", "Inventory"),
        ("inventory.category.create", "Create Category", "Inventory"),
        ("inventory.category.update", "Update Category", "Inventory"),
        ("inventory.category.delete", "Delete Category", "Inventory"),
        ("inventory.warehouse.create", "Create Warehouse", "Inventory"),
        ("inventory.warehouse.update", "Update Warehouse", "Inventory"),
        ("inventory.warehouse.delete", "Delete Warehouse", "Inventory"),
        ("inventory.stock.in", "Stock In", "Inventory"),
        ("inventory.stock.out", "Stock Out", "Inventory"),
        ("inventory.stock.adjust", "Stock Adjustment", "Inventory"),
        ("inventory.stock.transfer", "Stock Transfer", "Inventory"),
    ]
    
    perm_map = {}
    for code, name, module in permissions_data:
        p = db.query(Permission).filter(Permission.code == code).first()
        if not p:
            p = Permission(name=name, code=code, module=module)
            db.add(p)
            db.flush()
        perm_map[code] = p

    # Roles
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if not admin_role:
        admin_role = Role(name="ADMIN", description="Unrestricted enterprise administration")
        admin_role.permissions = list(perm_map.values())
        db.add(admin_role)
        db.flush()

    manager_role = db.query(Role).filter(Role.name == "MANAGER").first()
    if not manager_role:
        manager_role = Role(name="MANAGER", description="Operational Manager with full Inventory authority")
        manager_role.permissions = [
            p for code, p in perm_map.items()
            if code.startswith("inventory.") or code in ("AUTH_LOGIN", "USER_READ", "ROLE_READ")
        ]
        db.add(manager_role)
        db.flush()

    employee_role = db.query(Role).filter(Role.name == "EMPLOYEE").first()
    if not employee_role:
        employee_role = Role(name="EMPLOYEE", description="Standard Enterprise Employee")
        employee_role.permissions = [
            p for code, p in perm_map.items()
            if code in ("AUTH_LOGIN", "inventory.view")
        ]
        db.add(employee_role)
        db.flush()

    # Admin user
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            email="admin@smarterp.com",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("Admin@123"),
            is_active=True,
            is_superuser=True,
            roles=[admin_role]
        )
        db.add(admin_user)
    elif admin_user.email.endswith(".local"):
        admin_user.email = "admin@smarterp.com"

    # Manager user
    inv_user = db.query(User).filter(User.username == "inventory_manager").first()
    if not inv_user:
        inv_user = User(
            email="inventory@smarterp.com",
            username="inventory_manager",
            full_name="Inventory Manager",
            hashed_password=get_password_hash("Inventory@123"),
            is_active=True,
            is_superuser=False,
            roles=[manager_role]
        )
        db.add(inv_user)
    elif inv_user.email.endswith(".local"):
        inv_user.email = "inventory@smarterp.com"

    db.commit()

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    if db.query(User).count() == 0:
        seed_default_roles_and_admin(db)
        
    user = db.query(User).filter(
        (User.username == payload.username_or_email) | (User.email == payload.username_or_email)
    ).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        AuditService.log(
            db=db,
            action="FAILED_LOGIN",
            description=f"Failed login attempt for '{payload.username_or_email}'",
            ip_address=ip
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    if not user.is_active:
        AuditService.log(
            db=db,
            action="FAILED_LOGIN",
            description=f"Attempted login on inactive account '{user.username}'",
            user_id=user.id,
            ip_address=ip
        )
        raise HTTPException(status_code=400, detail="Account is disabled")

    # Record successful login
    AuditService.log(
        db=db,
        action="LOGIN",
        description=f"User '{user.username}' logged in successfully.",
        user_id=user.id,
        ip_address=ip
    )

    access_token = create_access_token(data={"sub": user.username})
    user_resp = UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
        roles=[r for r in user.roles],
        permissions=list(user.permissions)
    )
    return Token(access_token=access_token, token_type="bearer", user=user_resp)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists"
        )

    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username already exists"
        )

    new_user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active,
        is_superuser=False
    )

    # Assign default role if none specified
    if payload.roles:
        assigned = db.query(Role).filter(Role.name.in_(payload.roles)).all()
        new_user.roles = assigned
    else:
        emp_role = db.query(Role).filter(Role.name == "EMPLOYEE").first()
        if not emp_role:
            emp_role = db.query(Role).filter(Role.name == "MANAGER").first()
        if emp_role:
            new_user.roles = [emp_role]

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    AuditService.log(
        db=db,
        action="REGISTER",
        description=f"New user registered: '{new_user.username}' ({new_user.email})",
        user_id=new_user.id,
        ip_address=ip
    )

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        is_active=new_user.is_active,
        is_superuser=new_user.is_superuser,
        created_at=new_user.created_at,
        roles=[r for r in new_user.roles],
        permissions=list(new_user.permissions)
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        roles=[r for r in current_user.roles],
        permissions=list(current_user.permissions)
    )

@router.post("/logout")
def logout(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    AuditService.log(
        db=db,
        action="LOGOUT",
        description=f"User '{current_user.username}' logged out.",
        user_id=current_user.id,
        ip_address=ip
    )
    return {"message": "Logged out successfully"}

@router.get("/protected")
def protected_test_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "Access granted to protected endpoint",
        "username": current_user.username,
        "is_authenticated": True
    }

@router.get("/admin-only")
def admin_only_test_route(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser and not any(r.name == "ADMIN" for r in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")
    return {
        "message": "Access granted to admin-only endpoint",
        "username": current_user.username,
        "role": "ADMIN"
    }
