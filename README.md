# Reddit-Scraper-and-User-Psychoanalyze-On-Terrorism-Scale

This project is a Python-based tool that scrapes publicly available Reddit comments and uses AI to analyze users' comments to assess their vulnerability to extremist ideologies. The vulnerability score can be used to filter users or view their data, and users can be analyzed and processed automatically with the press of a button. The tool integrates with the HuggingChat API for the analysis.

---

## Features
- **Reddit Scraping**: Scrapes public posts and comments from a specified subreddit.
- **User Psychoanalysis**: Uses HuggingChat API to analyze user comments and assign a vulnerability score based on their expressed opinions and behavior.
- **AI Grading**: Users are graded on a scale assessing their potential vulnerability to extremist ideologies.
- **Database**: View, filter, and visualize user data, including vulnerability scores.
- **User Interface**: Built with PyQt5, providing a simple graphical interface for interaction with the tool.
- **Automation**: Scrape, analyze, and process data at the press of a button, including filtering users by their terrorism vulnerability score.

---

## Requirements
Before running the application, make sure to install the necessary dependencies by running:

```bash
pip install praw PyQt5 hugchat matplotlib numpy
```

This will install the following libraries:

- **`praw`**: Python Reddit API Wrapper for scraping Reddit data.
- **`PyQt5`**: Used to build the user interface.
- **`hugchat`**: For integrating with the HuggingChat API to perform user analysis.
- **`matplotlib`**: For visualizing data.
- **`numpy`**: For numerical operations.


## Setup
1. **Reddit Scraper Configuration**:  
   - Modify the `subreddit ID` in the `reddit_scraper.py` file to scrape the desired subreddit, and also the reddit bot credentials.
   
2. **HuggingChat API Credentials**:  
   - Add your HuggingChat credentials in the `analyze_users.py` file for AI-based analysis.
   
3. **Run the App**:  
   - To start the application, run the `main.py` file. This will launch the user interface with all functionalities integrated.

```bash
python main.py
```

---

## Features in Detail
### 1. **Reddit Scraping**  
   - Scrapes posts and comments from the specified subreddit. The `reddit_scraper.py` script is responsible for connecting to the Reddit API using the `praw` library and gathering publicly available posts and comments.

### 2. **User Psychoanalysis**  
   - The `analyze_users.py` script connects to the HuggingChat API, which is used to analyze the scraped comments. Based on the analysis, users are scored for their vulnerability to extremist ideologies.
   - The vulnerability score is a number that represents how much a user's content might align with extremist narratives.

### 3. **Data Viewing and Filtering**  
   - Once users are analyzed, their vulnerability scores can be viewed and filtered using the graphical interface.  
   - Data visualization tools are integrated to view the scores and trends within the collected data using `matplotlib`.

### 4. **Automation**  
   - The tool enables fully automated analysis with a simple button press, making it easy to scrape, analyze, and process large amounts of data in one go.

---

## Usage
1. **Run the app**:  
   - Execute the following command to launch the user interface:
   
   ```bash
   python main.py
   ```

2. **Interacting with the UI**:  
   - The UI allows users to:
     - Scrape data from Reddit using a specified subreddit.
     - View the scraped data and vulnerability scores.
     - Visualize user data and filter by vulnerability scores.
     - Process scraped data with a single button press for quick analysis.

3. **Filter by Vulnerability Score**:  
   - You can filter users by their vulnerability to terrorism score and choose to interact with those at higher risk levels.

---

## Future Enhancements
- **Refined AI Models**: Improve the AI models to more accurately detect subtle forms of extremist ideologies.
- **Integration with Other Data Sources**: Extend the tool to include data from other platforms or more subreddits.
- **Improved Visualization**: Develop more advanced data visualization tools to make the analysis more comprehensive.
- **User Interaction**: Allow for more granular control over data processing, such as custom scoring models or the ability to define what constitutes "vulnerable" behavior.

---

## Legal Disclaimer
Please ensure that you use this tool responsibly and comply with local laws and regulations regarding data privacy and ethical guidelines. This tool is intended for educational and research purposes only. Misuse of the tool for unethical or illegal purposes is strictly prohibited.

---

## Acknowledgments
- HuggingChat API for providing AI-based user analysis.
- PyQt5 for building the user interface.
- Praw for interacting with the Reddit API.
- Matplotlib and Numpy for data visualization and analysis.
 

---

thanks you guys!
-luna shoval 