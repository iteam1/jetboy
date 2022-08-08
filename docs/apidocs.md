### APIdocs

<details><summary>APIs</summary>
<p>

1. [Home](#Home)
2. [Stream color frame](#Stream-color-frame)
3. [Stream depth frame](#Stream-depth-frame)
4. [Stream both frame](#Stream-both-frame)

</p>
</details>

## Home [go to the top](#APIdocs)

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

## Stream color frame [go to the top](#APIdocs)

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

## Stream depth frame [go to the top](#APIdocs)

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

## Stream both frames [go to the top](#APIdocs)

  Response depth frame and color frame stack together
* **URL:** `/d`
* **Method:** `GET`
*  **URL Params:**
   **Required:**
    `None`
   **Optional:**
   `None`
* **Query Params:**`None`
* **Success Response:**
  * **Code:** 200 <br />
    **Content:** depth frame and color frame of depth camera
* **Error Response:**
  * **Code:** `None` <br />
    **Content:** `None`
* **Sample Call:**
* **Notes:**
  Get depth frame and color frame of depth camera real-time
