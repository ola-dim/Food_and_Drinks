CREATE TABLE IF NOT EXISTS food_drinks (
	id VARCHAR(255) PRIMARY KEY
	,name VARCHAR(255)
	,brewery_type VARCHAR(255)
	,street VARCHAR(255)
	,address_2 VARCHAR(255)
	,address_3 VARCHAR(255)
	,city VARCHAR(255)
	,state VARCHAR(255)
	,country_province VARCHAR(255)
	,postal_code VARCHAR(255)
	,website_url VARCHAR(255)
	,phone VARCHAR(255)
	,country VARCHAR(255)
	,longitude FLOAT
	,latitude FLOAT
	,tags VARCHAR(255)
	,rating FLOAT
	,number_of_ratings INTEGER
	,updated_at TIMESTAMP
	,created_at TIMESTAMP
);

-- Indexes for potential performance improvements
CREATE INDEX idx_brewery_type ON food_drinks (brewery_type);
CREATE INDEX idx_state ON food_drinks (state);
CREATE INDEX idx_rating ON food_drinks (rating);
CREATE INDEX idx_number_of_ratings ON food_drinks (number_of_ratings);
