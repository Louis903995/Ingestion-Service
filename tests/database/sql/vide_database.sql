-- drop achats.Enseignes
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.Enseignes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.Enseignes;
GO

-- drop achats.ProduitCategories 
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.ProduitCategories');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.ProduitCategories;
GO

-- drop achats.TicketEntetes
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.TicketEntetes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.TicketEntetes;
GO

-- drop achats.TicketLignes
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('achats.TicketLignes');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS achats.TicketLignes;
GO

DROP SCHEMA IF EXISTS achats;
GO

-- drop clients.clients
DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) +
    ' DROP CONSTRAINT ' + QUOTENAME(fk.name) + ';' + CHAR(13)
FROM sys.foreign_keys fk
INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE fk.referenced_object_id = OBJECT_ID('clients.clients');
IF @sql <> N''
    EXEC sp_executesql @sql;
DROP TABLE IF EXISTS clients.clients;
GO

DROP SCHEMA IF EXISTS clients;
GO