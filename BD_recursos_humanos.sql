CREATE DATABASE recursos_humanos;
USE recursos_humanos;

-- Tabla de países
CREATE TABLE paises (
    id_pais INT AUTO_INCREMENT PRIMARY KEY,
    nombre_pais VARCHAR(100) NOT NULL
);

-- Tabla de ciudades
CREATE TABLE ciudades (
    id_ciudad INT AUTO_INCREMENT PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES paises(id_pais)
);

-- Tabla de localizaciones
CREATE TABLE localizaciones (
    id_localizacion INT AUTO_INCREMENT PRIMARY KEY,
    direccion VARCHAR(255) NOT NULL,
    id_ciudad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
);

-- Tabla de departamentos
CREATE TABLE departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    id_localizacion INT NOT NULL,
    FOREIGN KEY (id_localizacion) REFERENCES localizaciones(id_localizacion)
);

-- Tabla de cargos
CREATE TABLE cargos (
    id_cargo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cargo VARCHAR(100) NOT NULL,
    salario DECIMAL(10, 2) NOT NULL
);

-- Tabla de empleados
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empleado VARCHAR(100) NOT NULL,
    apellido_empleado VARCHAR(100) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    id_ciudad INT NOT NULL,
    id_departamento INT NOT NULL,
    id_cargo INT NOT NULL,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_cargo) REFERENCES cargos(id_cargo)
);

-- Tabla de históricos
CREATE TABLE historicos (
    id_historico INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_operacion ENUM('insert', 'update', 'delete'),
    detalles_operacion TEXT,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);


-- Agregar datos a la tabla de países
INSERT INTO paises (nombre_pais) VALUES
('Colombia'),
('Estados Unidos'),
('España');

-- Agregar datos a la tabla de ciudades
INSERT INTO ciudades (nombre_ciudad, id_pais) VALUES
('Bogotá', 1),
('Medellín', 1),
('Nueva York', 2),
('Madrid', 3);

-- Agregar datos a la tabla de localizaciones
INSERT INTO localizaciones (direccion, id_ciudad) VALUES
('Calle 123, Barrio Centro', 1),
('Carrera 45, Barrio Sur', 2),
('5th Avenue, Manhattan', 3),
('Gran Vía 12', 4);

-- Agregar datos a la tabla de departamentos
INSERT INTO departamentos (nombre_departamento, id_localizacion) VALUES
('Recursos Humanos', 1),
('Tecnología', 2),
('Marketing', 3),
('Ventas', 4);

-- Agregar datos a la tabla de cargos
INSERT INTO cargos (nombre_cargo, salario) VALUES
('Gerente', 10000000.00),
('Desarrollador', 5000000.00),
('Analista', 4000000.00),
('Vendedor', 3000000.00);

-- Agregar datos a la tabla de empleados
INSERT INTO empleados (nombre_empleado, apellido_empleado, fecha_contratacion, direccion, id_ciudad, id_departamento, id_cargo, estado) VALUES
('Juan', 'Pérez', '2023-01-15', 'Calle 50, Barrio Norte', 1, 1, 1, 'activo'),
('María', 'González', '2022-05-10', 'Carrera 20, Barrio Este', 2, 2, 2, 'activo'),
('Carlos', 'Martínez', '2021-03-20', 'Calle 80, Barrio Oeste', 3, 3, 3, 'activo'),
('Ana', 'López', '2020-11-05', 'Calle 10, Barrio Sur', 4, 4, 4, 'activo');

-- (Opcional) Agregar datos iniciales a la tabla de históricos
-- Ejemplo para registrar una operación de inserción manualmente
INSERT INTO historicos (id_empleado, tipo_operacion, detalles_operacion) VALUES
(1, 'insert', 'Se agregó al empleado Juan Pérez con el cargo Gerente.');

SELECT * FROM paises;
SELECT * FROM ciudades;
SELECT * FROM localizaciones;
SELECT * FROM departamentos;
SELECT * FROM cargos;
SELECT * FROM empleados;
SELECT * FROM historico;
