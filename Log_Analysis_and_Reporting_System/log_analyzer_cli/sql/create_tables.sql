--create user_agents table
CREATE TABLE IF NOT EXISTS user_agents(
	id SERIAL PRIMARY KEY,
	user_agent_string TEXT UNIQUE NOT NULL,
	os VARCHAR(100),
	browser VARCHAR(100),
	device_type VARCHAR(100),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS log_entries(
	id SERIAL PRIMARY KEY,
	ip_address VARCHAR(45) NOT NULL,
	timestamp TIMESTAMP NOT NULL,
	method VARCHAR(10),
	path TEXT,
	status_code SMALLINT,
	bytes_sent INTEGER,
	referrer TEXT,
	user_agent_id INTEGER REFERENCES user_agents(id),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);