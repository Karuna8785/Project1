from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User, Role, Permission
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

def seed_default_roles_and_admin(db: Session):
    # Ensure inventory permissions exist
    permissions_data = [
        # Inventory permissions
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
        # Other module view permissions
        ("hr.view", "View HR", "HR"),
        ("crm.view", "View CRM", "CRM"),
        ("sales.view", "View Sales", "Sales"),
        ("procurement.view", "View Procurement", "Procurement"),
        ("reports.view", "View Reports", "Reports"),
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
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        admin_role = Role(name="Admin", description="Full system access across all ERP modules")
        admin_role.permissions = list(perm_map.values())
        db.add(admin_role)
        db.flush()

    inventory_role = db.query(Role).filter(Role.name == "Inventory Manager").first()
    if not inventory_role:
        inventory_role = Role(name="Inventory Manager", description="Manage inventory, products, categories, warehouses and stock")
        inventory_role.permissions = [p for code, p in perm_map.items() if code.startswith("inventory.") or code in ("reports.view", "sales.view", "procurement.view")]
        db.add(inventory_role)
        db.flush()

    # Admin user
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            email="admin@smarterp.local",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("Admin@123"),
            is_active=True,
            is_superuser=True,
            roles=[admin_role]
        )
        db.add(admin_user)

    # Inventory Manager user
    inv_user = db.query(User).filter(User.username == "inventory_manager").first()
    if not inv_user:
        inv_user = User(
            email="inventory@smarterp.local",
            username="inventory_manager",
            full_name="Inventory Specialist",
            hashed_password=get_password_hash("Inventory@123"),
            is_active=True,
            is_superuser=False,
            roles=[inventory_role]
        )
        db.add(inv_user)

    db.commit()

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # Auto-seed defaults if database is fresh
    if db.query(User).count() == 0:
        seed_default_roles_and_admin(db)
        
    user = db.query(User).filter(
        (User.username == payload.username_or_email) | (User.email == payload.username_or_email)
    ).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled")

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

@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists"
        )
    
    new_user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active,
        is_superuser=False
    )
    
    # Assign roles if provided
    if payload.roles:
        assigned = db.query(Role).filter(Role.name.in_(payload.roles)).all()
        new_user.roles = assigned
    else:
        inv_role = db.query(Role).filter(Role.name == "Inventory Manager").first()
        if inv_role:
            new_user.roles = [inv_role]

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
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
