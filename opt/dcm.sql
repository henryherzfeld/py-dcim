CREATE DATABASE dcm;

USE dcm;


CREATE TABLE row (
       row_id VARCHAR(1) NOT NULL PRIMARY KEY
);

CREATE TABLE rack (
       rack_id INT(3) NOT NULL AUTO_INCREMENT PRIMARY KEY,
       row_id VARCHAR(1) NOT NULL,
       rack_number VARCHAR(2) NOT NULL,
       rack_desc VARCHAR(30),
       UNIQUE(rack_id, row_id),
       FOREIGN KEY(row_id) REFERENCES row(row_id) ON DELETE CASCADE
);


CREATE TABLE ups1 (
       rack_id INT(3) NOT NULL,
       reading_dt DATETIME NOT NULL,

       nominal_voltage INT(4),  
       input_frequency INT(2),
       output_frequency INT(2),
       input_voltage_1_phase_1 INT(4),
       input_voltage_1_phase_2 INT(4),
       input_voltage_1_phase_3 INT(4),
       input_voltage_2_phase_1 INT(4),
       input_voltage_2_phase_2 INT(4),
       input_voltage_2_phase_3 INT(4),
       input_current_1_phase_1 NUMERIC(5,1),
       input_current_1_phase_2 NUMERIC(5,1),
       input_current_1_phase_3 NUMERIC(5,1),
       output_current_phase_1 INT(4),
       output_current_phase_2 INT(4),
       output_current_phase_3 INT(4),
       output_voltage_phase_1 INT(4),
       output_voltage_phase_2 INT(4),
       output_voltage_phase_3 INT(4),
       
       FOREIGN KEY(rack_id) REFERENCES rack(rack_id) ON DELETE CASCADE
);

CREATE TABLE ups2 (
       rack_id INT(3) NOT NULL,
       reading_dt DATETIME NOT NULL,

       output_frequency NUMERIC(3,1),
       input_voltage_ltol_phase_1 NUMERIC(4,1),
       input_voltage_ltol_phase_2 NUMERIC(4,1),
       input_voltage_ltol_phase_3 NUMERIC(4,1),
       output_voltage_ltol_phase_1 NUMERIC(4,1),
       output_voltage_ltol_phase_2 NUMERIC(4,1),
       output_voltage_ltol_phase_3 NUMERIC(4,1),
       output_voltage_lton_phase_1 NUMERIC(4,1),
       output_voltage_lton_phase_2 NUMERIC(4,1),
       output_voltage_lton_phase_3 NUMERIC(4,1),
       output_current_ltol_phase_1 NUMERIC(4,1),
       output_current_ltol_phase_2 NUMERIC(4,1),
       output_current_ltol_phase_3 NUMERIC(4,1),
       output_power_ltol_phase_1 INT(4),
       output_power_ltol_phase_2 INT(4),
       output_power_ltol_phase_3 INT(4),
       output_power_factor_ltol_phase_1 NUMERIC(3,2),
       output_power_factor_ltol_phase_2 NUMERIC(3,2),
       output_power_factor_ltol_phase_3 NUMERIC(3,2),

       FOREIGN KEY(rack_id) REFERENCES rack(rack_id) ON DELETE CASCADE
);


CREATE TABLE rpdu (
       rack_id INT(3) NOT NULL,
       reading_dt DATETIME NOT NULL,

       pdua_power INT(4),
       pdua_power_factor NUMERIC(5,4),
       pdua_ltol_voltage INT(4),
       pdub_power INT(4),
       pdub_power_factor NUMERIC(5,4),
       pdub_ltol_voltage INT(4),
       temp NUMERIC(3,1),
       temp2 NUMERIC(3,1),
       humi NUMERIC(3,1),

       FOREIGN KEY(rack_id) REFERENCES rack(rack_id) ON DELETE CASCADE
);


CREATE TABLE inlinerp (
       rack_id INT(3) NOT NULL,
       reading_dt DATETIME NOT NULL,

       rack_inlet_temp NUMERIC(3,1),
       supply_air_temp NUMERIC(3,1),
       return_air_temp NUMERIC(3,1),

       compressor_drive_power INT(4),
       compressor_drive_voltage NUMERIC(4,1),
       compressor_drive_current NUMERIC(4,1),

       FOREIGN KEY(rack_id) REFERENCES rack(rack_id) ON DELETE CASCADE
);



INSERT INTO row (row_id) VALUES ('A');
INSERT INTO row (row_id) VALUES ('B');

INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('2','UPS1', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('3','UPS2', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('4','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('5','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('6','INLINE RP AC', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('7','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('8','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('9','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('10','INLINE RP AC', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('11','RACK PDU', 'A');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('12','RACK PDU', 'A');

INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('2','UPS1', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('3','UPS2', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('4','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('5','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('6','INLINE RP AC', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('7','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('8','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('9','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('10','INLINE RP AC', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('11','RACK PDU', 'B');
INSERT INTO rack (rack_number,rack_desc, row_id) VALUES ('12','RACK PDU', 'B');

-- 'YYYY-MM-DD HH:MM:SS'

-- INSERT INTO reading (rack_id, reading_name, reading_dt, reading_value) VALUES ('1','Real Voltage', '2018-01-22 08:23:16', '217');

SELECT min(mx)
FROM (
      SELECT max(reading_dt) AS `mx` FROM ups1
      UNION
      SELECT max(reading_dt) AS `mx` FROM ups2
      UNION
      SELECT max(reading_dt) AS `mx` FROM rpdu
      UNION
      SELECT max(reading_dt) AS `mx` FROM rpdu_env
      UNION
      SELECT max(reading_dt) AS `mx` FROM inlinerp
     ) AS t1


