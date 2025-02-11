CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,

    cashback DECIMAL NOT NULL,
    cashback_value_type VARCHAR(255) NOT NULL,

    cashback_change_last_24h DECIMAL DEFAULT NULL,
    cashback_change_last_7d  DECIMAL DEFAULT NULL,
    cashback_change_last_30d DECIMAL DEFAULT NULL,

    cashback_lowest DECIMAL DEFAULT NULL,
    cashback_highest DECIMAL DEFAULT NULL,

    cashback_path VARCHAR(255) NOT NULL
);

CREATE INDEX merchants_name_index ON merchants (name);
