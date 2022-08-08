### APIs

1. [Home](#Home)
2. [Stream color frame](#Stream_color_frame)
2. [Stream depth frame](#Stream_depth_frame)

#### Home
----
  Home page
* **URL:** `/`
* **Method:** `GET`
*  **URL Params:**
   **Required:**
    `None`
   **Optional:**
   `None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** `home.html`
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Check server is alive or not.

#### Stream color frame
----
  Response color frame from depth camera
* **URL:** `/color`
* **Method:** `GET`
*  **URL Params:**
   **Required:**
    `None`
   **Optional:**
   `None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** streaming color frame
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get color frame of depth camera real-time

#### Stream depth frame
----
  Response depth frame from depth camera
* **URL:** `/depth`
* **Method:** `GET`
*  **URL Params:**
   **Required:**
    `None`
   **Optional:**
   `None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** streaming depth frame
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get depth frame of depth camera real-time