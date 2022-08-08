### APIdocs

1. [Home](#Home)
2. [Stream color frame](#Stream-color-frame)
3. [Stream depth frame](#Stream-depth-frame)
4. [Stream both frames](#Stream-both-frames)

## Home
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

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
</p>
</details>

## Stream color frame
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

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
</p>
</details>

## Stream depth frame
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

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
</p>
</details>

## Stream both frames
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Response depth frame and color frame stack together
* **URL:** `/both`
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
</p>
</details>

## Manual
[go back](#APIdocs)
<details><summary>click to expand</summary>
<p>

  Return a GUI as manual panel for controlling
* **URL:** `/manual`
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
</p>
</details>