-- ============================================================
-- Migración 2: fecha de nacimiento + calificaciones
-- No borra ninguna tabla ni dato existente. Segura de repetir.
--
-- Cómo usarla en phpMyAdmin:
--   1. Entra a tu base de datos "obra_conecta"
--   2. Pestaña "SQL"
--   3. Pega todo este archivo y dale "Continuar"
-- ============================================================

ALTER TABLE `usuarios`
  ADD COLUMN IF NOT EXISTS `fecha_nacimiento` DATE NULL AFTER `foto_url`;

CREATE TABLE IF NOT EXISTS `calificaciones` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `solicitud_id` INT(11) NOT NULL,
  `cliente_id` INT(11) NOT NULL,
  `profesional_id` INT(11) NOT NULL,
  `puntuacion` INT(11) NOT NULL,
  `comentario` TEXT NULL,
  `fecha` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `solicitud_id` (`solicitud_id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `profesional_id` (`profesional_id`),
  CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`solicitud_id`) REFERENCES `solicitudes_trabajo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `calificaciones_ibfk_3` FOREIGN KEY (`profesional_id`) REFERENCES `profesionales` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
