-- ============================================================
--  Base de datos generada desde el diagrama ER
-- ============================================================

CREATE DATABASE IF NOT EXISTS base
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE base;

-- ------------------------------------------------------------
-- Tabla: usuarios
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario  INT          NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(100) NOT NULL,
    correo      VARCHAR(100) NOT NULL,
    contraseña  VARCHAR(255) NOT NULL,
    rol         VARCHAR(50)  NOT NULL,
    PRIMARY KEY (id_usuario),
    UNIQUE KEY uq_usuarios_correo (correo)
);

-- ------------------------------------------------------------
-- Tabla: apoyos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS apoyos (
    id_apoyo    INT          NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(150) NOT NULL,
    tipo        VARCHAR(100),
    descripcion TEXT,
    requisitos  TEXT,
    ubicacion   VARCHAR(150),
    enlace      VARCHAR(255),
    PRIMARY KEY (id_apoyo)
);

-- ------------------------------------------------------------
-- Tabla: documentos_rag
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documentos_rag (
    id_documento    INT          NOT NULL AUTO_INCREMENT,
    nombre_documento VARCHAR(255) NOT NULL,
    contenido       LONGTEXT,
    embedding_id    VARCHAR(255),
    PRIMARY KEY (id_documento)
);

-- ------------------------------------------------------------
-- Tabla: embeddings
-- (id_documento referencia documentos_rag)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS embeddings (
    id_embedding    INT      NOT NULL AUTO_INCREMENT,
    id_documento    INT      NOT NULL,
    embedding       JSON,                  -- Se almacena como JSON; usa VECTOR si tu motor lo soporta
    metadatos       JSON,
    fecha_creacion  DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_embedding),
    CONSTRAINT fk_embeddings_documento
        FOREIGN KEY (id_documento)
        REFERENCES documentos_rag (id_documento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- Tabla: historial_chat
-- (id_usuario referencia usuarios)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historial_chat (
    id_chat     INT      NOT NULL AUTO_INCREMENT,
    id_usuario  INT      NOT NULL,
    pregunta    TEXT,
    respuesta   TEXT,
    fecha       DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_chat),
    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- Tabla: logs_sistema
-- (usuario referencia apoyos según el diagrama —
--  la línea discontinua llega desde apoyos)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS logs_sistema (
    id_log   INT          NOT NULL AUTO_INCREMENT,
    accion   VARCHAR(255),
    fecha    DATETIME     DEFAULT CURRENT_TIMESTAMP,
    usuario  VARCHAR(100),
    PRIMARY KEY (id_log)
);

CREATE TABLE becas (
    id_beca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    categoria ENUM('educacion','bienestar','vivienda','empleo','alimentacion','adultos_mayores') NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    pdf VARCHAR(255)
);
-- ============================================================
--  Índices adicionales recomendados
-- ============================================================
CREATE INDEX idx_historial_usuario   ON historial_chat  (id_usuario);
CREATE INDEX idx_embeddings_documento ON embeddings      (id_documento);
CREATE INDEX idx_logs_fecha          ON logs_sistema     (fecha);
