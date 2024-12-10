# Model-Driven Test Design (Input Domain Model and/or Control Flow Graph)

## ISP Documentation for `get_image_external`

### Input Domain Model

| Characteristics    | b1              | b2           | b3           |
|--------------------|-----------------|--------------|--------------|
| Query Validity     | Valid URL       | Invalid URL  | Empty String |
| Infobox Presence   | Infobox Present | Infobox Absent | N/A         |
| Image Tag Presence | Image Tag Present | Image Tag Absent | N/A      |

#### Explanation for Choosing this Input Domain Model

- **Query Validity**: Ensures the function handles various types of input (valid, invalid, and empty).
- **Infobox Presence**: Tests if the infobox element is correctly identified or its absence is handled.
- **Image Tag Presence**: Ensures correct behavior when an `img` tag exists or is missing in the infobox.

### IDM Relabeling Table

| Characteristics    | b1  | b2  | b3  |
|--------------------|------|------|------|
| Query Validity     | (Q1) | (Q2) | (Q3) |
| Infobox Presence   | (I1) | (I2) | (I3) |
| Image Tag Presence | (T1) | (T2) | (T3) |

### Constraints

- Query must be a string.
- URL validation is not performed within the function; it relies on the behavior of `requests.get`.
- If the query is invalid, subsequent conditions on infobox and `img` tags are irrelevant.

### Test Values and Example I/O

Criteria Used: **Edge Coverage**

| Test Value | Example Input                              | Expected Output       |
|------------|--------------------------------------------|-----------------------|
| Q1I1T1     | `http://validurl.com` with infobox & image | Image URL (`img["src"]`) |
| Q1I1T2     | `http://validurl.com` with infobox but no image | None               |
| Q1I2T3     | `http://validurl.com` with no infobox      | None                 |
| Q2I3T3     | `invalid-url`                              | None                 |
| Q3I3T3     | `""` (empty string)                       | None                 |

### Associate Test Paths with Existing Test Cases for IDM

1. **Test Value: Q1I1T1**
   - Test Case: `test_valid_url_with_infobox_and_image`
   - Explanation: Validates the full path where a valid query contains both an infobox and an image tag.

2. **Test Value: Q1I1T2**
   - Test Case: `test_valid_url_with_infobox_no_image`
   - Explanation: Ensures the function handles an infobox without an image correctly.

3. **Test Value: Q1I2T3**
   - Test Case: `test_valid_url_no_infobox`
   - Explanation: Confirms the function returns `None` if no infobox exists.

4. **Test Value: Q2I3T3**
   - Test Case: `test_invalid_url`
   - Explanation: Checks behavior when an invalid URL is passed.

5. **Test Value: Q3I3T3**
   - Test Case: `test_empty_query`
   - Explanation: Verifies handling of an empty query.

## Control Flow Graph (CFG) for `get_image_external`

### Test Requirements (Edge-Pair Coverage)

1. Edge (`start -> try`) - Entry to the `try` block.
2. Edge (`try -> response.raise_for_status`) - Making the HTTP GET request.
3. Edge (`response.raise_for_status -> soup.find`) - Successful request.
4. Edge (`soup.find -> return None`) - No infobox present.
5. Edge (`soup.find -> infobox.find`) - Infobox found.
6. Edge (`infobox.find -> return image_tag["src"]`) - Image found in the infobox.
7. Edge (`infobox.find -> return None`) - No image in the infobox.
8. Edge (`try -> except`) - Exception handling.
9. Edge (`except -> return None`) - Catch-all exception handling.

### Test Paths

1. `[start, try, response.raise_for_status, soup.find, infobox.find, return image_tag["src"]]` - Full valid path.
2. `[start, try, response.raise_for_status, soup.find, return None]` - Valid query, no infobox.
3. `[start, try, response.raise_for_status, soup.find, infobox.find, return None]` - Valid query, infobox without image.
4. `[start, try, except, return None]` - Exception during HTTP request.
5. `[start, try, return None]` - Empty query.

### Associate Test Paths with Existing Test Cases for CFG

1. **Path 1**
   - Test Case: `test_valid_url_with_infobox_and_image`
   - Explanation: Covers the successful case with an image returned.

2. **Path 2**
   - Test Case: `test_valid_url_no_infobox`
   - Explanation: Confirms handling of a valid query with no infobox.

3. **Path 3**
   - Test Case: `test_valid_url_with_infobox_no_image`
   - Explanation: Handles a valid query with an infobox but no image.

4. **Path 4**
   - Test Case: `test_invalid_url`
   - Explanation: Ensures exception handling for invalid queries.

5. **Path 5**
   - Test Case: `test_empty_query`
   - Explanation: Verifies handling of an empty query.
