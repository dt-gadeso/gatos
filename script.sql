-- Cat Colony Management System Database Schema
-- Fixed and organized version

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS visit_services CASCADE;
DROP TABLE IF EXISTS visits CASCADE;
DROP TABLE IF EXISTS observations CASCADE;
DROP TABLE IF EXISTS cats CASCADE;
DROP TABLE IF EXISTS colonies CASCADE;
DROP TABLE IF EXISTS agreements CASCADE;
DROP TABLE IF EXISTS vet_services CASCADE;
DROP TABLE IF EXISTS vet_centers CASCADE;
DROP TABLE IF EXISTS councils CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS municipalities CASCADE;
DROP TABLE IF EXISTS zones CASCADE;
DROP TABLE IF EXISTS managers CASCADE;
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS associations CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- Drop custom types if they exist
DROP TYPE IF EXISTS sex_type CASCADE;

-- Create custom types
CREATE TYPE sex_type AS ENUM ('M', 'F');

-- Create tables in dependency order

CREATE TABLE IF NOT EXISTS roles(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    email_verified_at TIMESTAMP DEFAULT NULL,
    role_id INT,
    avatar_file VARCHAR(255) DEFAULT NULL,
    volunteer_number VARCHAR(50) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_role_id 
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS associations(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    association_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_members_user_id 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_members_association_id 
        FOREIGN KEY (association_id) REFERENCES associations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS managers(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    association_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_managers_user_id 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_managers_association_id
        FOREIGN KEY (association_id) REFERENCES associations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS zones(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS municipalities(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    zone_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_municipalities_zone_id
        FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS locations(
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    municipality_id INT NOT NULL,
    latitude DECIMAL(10, 8) DEFAULT NULL,
    longitude DECIMAL(11, 8) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_locations_municipality_id
        FOREIGN KEY (municipality_id) REFERENCES municipalities(id) ON DELETE CASCADE   
);

CREATE TABLE IF NOT EXISTS councils(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    emergency_email VARCHAR(100) NOT NULL,
    emergency_phone VARCHAR(15) NOT NULL,
    logo_file VARCHAR(255) DEFAULT NULL,
    location_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_councils_location_id 
        FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vet_centers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    logo_file VARCHAR(255) DEFAULT NULL,
    location_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_vet_centers_location_id 
        FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS agreements(
    id SERIAL PRIMARY KEY,
    council_id INT NOT NULL,
    vet_center_id INT NOT NULL,
    week_days INT NOT NULL CHECK (week_days >= 0 AND week_days <= 7),
    week_cats INT NOT NULL CHECK (week_cats >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_agreements_council_id 
        FOREIGN KEY (council_id) REFERENCES councils(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_agreements_vet_center_id
        FOREIGN KEY (vet_center_id) REFERENCES vet_centers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vet_services(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS colonies(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_id INT NOT NULL,
    manager_id INT,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_colonies_location_id 
        FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_colonies_manager_id
        FOREIGN KEY (manager_id) REFERENCES managers(id) ON DELETE SET NULL,
    
    CONSTRAINT fk_colonies_user_id
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cats(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    photo_file VARCHAR(255) DEFAULT NULL,
    chip VARCHAR(50) UNIQUE,
    birthday DATE DEFAULT NULL,
    sex sex_type NOT NULL, 
    sterilized BOOLEAN NOT NULL DEFAULT FALSE,
    dead BOOLEAN NOT NULL DEFAULT FALSE,
    colony_id INT DEFAULT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cats_colony_id 
        FOREIGN KEY (colony_id) REFERENCES colonies(id) ON DELETE SET NULL,
    
    CONSTRAINT fk_cats_user_id
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS visits(
    id SERIAL PRIMARY KEY,
    cat_id INT NOT NULL,
    vet_center_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    report_file VARCHAR(255) NOT NULL,
    bill_file VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    visit_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_visits_cat_id
        FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_visits_vet_center_id
        FOREIGN KEY (vet_center_id) REFERENCES vet_centers(id) ON DELETE CASCADE,

    CONSTRAINT fk_visits_user_id
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS visit_services(
    id SERIAL PRIMARY KEY,
    visit_id INT NOT NULL,
    vet_service_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_visit_services_visit_id 
        FOREIGN KEY (visit_id) REFERENCES visits(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_visit_services_vet_service_id
        FOREIGN KEY (vet_service_id) REFERENCES vet_services(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS observations(
    id SERIAL PRIMARY KEY,
    cat_id INT NOT NULL,
    observation TEXT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_observations_cat_id 
        FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE,
    
    CONSTRAINT fk_observations_user_id
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);