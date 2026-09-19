-- ============================================================
-- Migración: perfil completo de profesionales
-- Agrega las columnas nuevas sin borrar ninguna tabla ni dato
-- existente. Es seguro correrlo aunque ya lo hayas corrido antes
-- (usa IF NOT EXISTS en cada columna).
--
-- Cómo usarlo en phpMyAdmin:
--   1. Entra a tu base de datos "obra_conecta"
--   2. Pestaña "SQL"
--   3. Pega todo este archivo y dale "Continuar"
-- ============================================================

ALTER TABLE `profesionales`
  ADD COLUMN IF NOT EXISTS `especialidad_principal` VARCHAR(120) NULL AFTER `descripcion`,
  ADD COLUMN IF NOT EXISTS `otras_habilidades` TEXT NULL AFTER `especialidad_principal`,
  ADD COLUMN IF NOT EXISTS `certificaciones` TEXT NULL AFTER `otras_habilidades`,
  ADD COLUMN IF NOT EXISTS `zonas_atencion` VARCHAR(255) NULL AFTER `certificaciones`,
  ADD COLUMN IF NOT EXISTS `nivel_experiencia` VARCHAR(40) NULL AFTER `zonas_atencion`,
  ADD COLUMN IF NOT EXISTS `rol_equipo` VARCHAR(80) NULL AFTER `nivel_experiencia`,
  ADD COLUMN IF NOT EXISTS `coordinador_id` INT(11) NULL AFTER `rol_equipo`;

-- Llave foránea del coordinador (un profesional puede reportarle a otro).
-- Si ya existe, este bloque simplemente fallará con un aviso que puedes
-- ignorar (significa que ya estaba creada).
ALTER TABLE `profesionales`
  ADD CONSTRAINT `profesionales_coordinador_fk`
  FOREIGN KEY (`coordinador_id`) REFERENCES `profesionales` (`id`)
  ON DELETE SET NULL;
