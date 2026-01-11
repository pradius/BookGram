### Post API: `SaveFile`

**Endpoint Overview**
* **Method:** `POST`
* **Target:** `file_service` & `user_service`
* **Returns:** `Topic`

---

### Request Handling
* **Inputs:**
    * **File:** Any text format (supports compressed / chunks).
    * **Title:** String (will be stored as a normalized **Topic** in the DB).
* **Validations:**
    * Check for corrupted files.
    * Ensure title is non-empty.

---

### Business Logic

#### 1. File Service (`file_service`)
* **Disk Storage:**
    * Saves the file to the local filesystem.
    * Generates and returns a `location_url` (normalized by title).
* **Database Storage (`Files` Table):**
    * `location_url`: Path to the file on disk.
    * `topic`: Normalized title.
    * `size`: File size in bytes.
    * `format`: File extension/type.
    * `chapters`: Default to empty list/null.
    * `pages`: Default to empty list/null.

#### 2. User Service (`user_service`)
* **Subscription Logic:**
    * Passes the **Topic** to the service.
    * Subscribes the current user to the **Topic** in the `User` database table.