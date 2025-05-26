<h1>Geotechnical Data Migration and Cleaning</h1>
youtube demo: https://youtu.be/AU6s36JFmeg

<p>
  This project is focused on migrating geotechnical engineering data from Excel spreadsheets to a MySQL database, using CSV as an intermediate format. The goal is to automate and standardize the data cleaning process to ensure accurate, clean, and structured data storage.
</p>

<h2>Key Features</h2>
<ul>
  <li><strong>Data Cleaning:</strong> Convert inconsistent data (e.g. "12,3", "abc", None) into standardized numeric formats for proper analysis.</li>
  <li><strong>CSV Transformation:</strong> Excel files are first cleaned and exported to CSV format for validation.</li>
  <li><strong>Database Integration:</strong> Cleaned data is migrated into a MySQL database for further analysis and querying.</li>
  <li><strong>Automated Testing:</strong> Unit tests ensure the data cleaning functions perform as expected.</li>
</ul>

<h2>Test Coverage</h2>
<p>The included test functions cover:</p>
<ul>
  <li><code>clean_mpa_column</code>: Cleans a single MPa column by handling decimal commas, invalid strings, and missing values.</li>
  <li><code>clean_all_mpa_columns</code>: Applies MPa cleaning to all relevant columns (e.g., 15M_MPa, 30M_MPa).</li>
  <li><code>clean_shotcrete_layer</code>: Converts shotcrete layer values to float, handling invalid or missing entries.</li>
</ul>

<h2>Technologies Used</h2>
<ul>
  <li>Python 3</li>
  <li>pandas</li>
  <li>MySQL</li>
  <li>pytest (for testing)</li>
</ul>

<h2>Getting Started</h2>
<ol>
  <li>Clone the repository.</li>
  <li>Install dependencies using <code>pip install -r requirements.txt</code>.</li>
  <li>Run tests using <code>pytest</code> to ensure everything works correctly.</li>
  <li>Prepare your Excel files and run the cleaning/migration script.</li>
</ol>

<h2>Author</h2>
<p>Developed by a geotechnical engineer to streamline data workflows in mining and civil projects.</p>
