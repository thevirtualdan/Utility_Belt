USE [DATABASE_NAME];
GO

DECLARE @TableName NVARCHAR(255);
DECLARE @IndexName NVARCHAR(255);
DECLARE @SchemaName NVARCHAR(255);

DECLARE table_cursor CURSOR FOR
SELECT t.name AS TableName, i.name AS IndexName, s.name AS SchemaName
FROM sys.tables t
JOIN sys.indexes i ON t.object_id = i.object_id
JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE i.type_desc IN ('CLUSTERED', 'NONCLUSTERED'); -- Only reorganize clustered and nonclustered indexes

OPEN table_cursor;

FETCH NEXT FROM table_cursor INTO @TableName, @IndexName, @SchemaName;

WHILE @@FETCH_STATUS = 0
BEGIN
    DECLARE @ReorganizeSQL NVARCHAR(MAX);
    SET @ReorganizeSQL = 'ALTER INDEX ' + QUOTENAME(@IndexName) + ' ON ' + QUOTENAME(@SchemaName) + '.' + QUOTENAME(@TableName) + ' REORGANIZE;';
    EXEC (@ReorganizeSQL);
    
    FETCH NEXT FROM table_cursor INTO @TableName, @IndexName, @SchemaName;
END;

CLOSE table_cursor;
DEALLOCATE table_cursor;
