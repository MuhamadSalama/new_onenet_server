# API Documentation Export Guide

## How to Export the API Specification

### Step 1: Run the Export Script
```bash
cd new_onenet_server
python export_openapi.py
```

This will generate `onenet_api_spec.json` in the same folder.

---

## How the Frontend Team Can Use This File

### Option 1: Import into Postman (Recommended)
1. Open Postman
2. Click **Import** (top left)
3. Select **Upload Files**
4. Choose `onenet_api_spec.json`
5. Postman will automatically create a collection with all endpoints

**Benefits:**
- All endpoints are ready to test
- Request/response schemas are pre-filled
- Easy to test authentication flows

### Option 2: Import into Swagger UI (Online Viewer)
1. Go to https://editor.swagger.io/
2. Click **File → Import file**
3. Upload `onenet_api_spec.json`
4. The API documentation will be displayed interactively

### Option 3: Use with API Client Libraries
Frontend developers can use the OpenAPI spec to auto-generate TypeScript/JavaScript clients:

**For TypeScript (React/Next.js):**
```bash
npx openapi-typescript-codegen --input onenet_api_spec.json --output ./src/api
```

**For JavaScript (Axios):**
```bash
npx swagger-typescript-api -p onenet_api_spec.json -o ./src/api
```

---

## What's Included in the Spec

The JSON file contains:
- ✅ All endpoint paths (`/auth/login`, `/users`, etc.)
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Request body schemas (required fields, types, validation)
- ✅ Response schemas (success and error formats)
- ✅ Authentication requirements (cookies, headers)
- ✅ Query parameters and path parameters
- ✅ Pydantic model definitions

---

## Updating the Spec

If you add new endpoints or modify schemas:
1. Make your changes to the FastAPI code
2. Run `python export_openapi.py` again
3. Share the updated `onenet_api_spec.json` with the frontend team

The spec is automatically generated from your Pydantic models and route definitions!
