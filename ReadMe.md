Hello

```mermaid
erDiagram
    STAFF {
        integer id PK
        varchar(50) first_name
        varchar(50) last_name
        varchar(30) role
        varchar(100) email
        varchar(20) phone
        timestamp created_at
        timestamp updated_at
    }

    RESTAURANT_TABLES {
        integer id PK
        varchar(10) table_number
        integer capacity
        varchar(50) location
        varchar(20) status
        timestamp created_at
        timestamp updated_at
    }

    MENU_ITEMS {
        integer id PK
        varchar(100) name
        text description
        varchar(50) category
        decimal price
        decimal cost
        boolean is_available
        integer preparation_time
        timestamp created_at
        timestamp updated_at
    }

    INVENTORY {
        integer id PK
        varchar(100) item_name
        varchar(50) category
        decimal(10,3) quantity
        varchar(20) unit
        varchar(100) supplier
        date last_restock_date
        date next_restock_date
        decimal(10,3) min_quantity
        varchar(20) status
        timestamp created_at
        timestamp updated_at
    }

    ORDERS {
        integer id PK
        integer table_id FK
        integer staff_id FK
        timestamp order_time
        varchar(20) status
        decimal(10,2) total_amount
        varchar(30) payment_method
        varchar(20) payment_status
        text notes
        timestamp created_at
        timestamp updated_at
    }

    ORDER_ITEMS {
        integer id PK
        integer order_id FK
        integer menu_item_id FK
        integer quantity
        text special_instructions
        varchar(20) status
        timestamp created_at
        timestamp updated_at
    }

    STAFF_SCHEDULES {
        integer id PK
        integer staff_id FK
        date shift_date
        time start_time
        time end_time
        varchar(20) status
        timestamp created_at
        timestamp updated_at
    }

    RESERVATIONS {
        integer id PK
        integer table_id FK
        varchar(100) customer_name
        varchar(20) customer_phone
        varchar(100) customer_email
        timestamp reservation_time
        integer party_size
        varchar(20) status
        text special_requests
        timestamp created_at
    }

    INVENTORY_USAGE {
        integer id PK
        integer inventory_id FK
        integer menu_item_id FK
        decimal(10,3) quantity_used
        date usage_date
        integer staff_id FK
        text notes
        timestamp created_at
    }

    STAFF ||--o{ ORDERS : "takes"
    STAFF ||--o{ STAFF_SCHEDULES : "has"
    STAFF ||--o{ INVENTORY_USAGE : "records"
    RESTAURANT_TABLES ||--o{ ORDERS : "hosts"
    RESTAURANT_TABLES ||--o{ RESERVATIONS : "reserved_for"
    MENU_ITEMS ||--o{ ORDER_ITEMS : "ordered_as"
    MENU_ITEMS ||--o{ INVENTORY_USAGE : "uses"
    ORDERS ||--o{ ORDER_ITEMS : "contains"
    INVENTORY ||--o{ INVENTORY_USAGE : "tracked_in"
```
