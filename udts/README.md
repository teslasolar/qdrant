# User Defined Types (UDTs) for Tag System

Reusable JSON schema definitions to reduce tag file sizes and maintain consistency.

## Available UDTs

### tag-base.json
Base structure for all tag.json files with required fields:
- UUID, ISA_Level, Directory_Path, Title
- Color_Scheme, Icon, Description
- Parent_Path

### feature.json
Feature definition (max 50 char title, 200 char description):
```json
{
  "title": "Feature Name",
  "description": "Brief description",
  "icon": "🔧"
}
```

### child-directory.json
Child directory reference:
```json
{
  "path": "/path/",
  "title": "Name",
  "description": "Description",
  "icon": "📁",
  "page_count": 10
}
```

### quick-action.json
Quick action button:
```json
{
  "label": "Action Name",
  "path": "file.html",
  "type": "primary"
}
```

## Usage

Reference UDTs in your tag files:
```json
{
  "$ref": "/udts/tag-base.json",
  "UUID": "unique-id",
  "Title": "My Component",
  "Features": [
    {"$ref": "/udts/feature.json"}
  ]
}
```

## Benefits

- Reduced file sizes (50-70% smaller)
- Consistent structure across all tags
- Easier validation and maintenance
- Clear field length limits
- Reusable components
