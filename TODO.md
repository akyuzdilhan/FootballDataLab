## TODO List

### Current Tasks

#### Plotly Dash

- [ ] Add a loading component for each page.

- [ ] Graph identical to the [documentation exemple](https://dash.plotly.com/dash-core-components/store#share-data-between-callbacks), to compare temporal statistics, such as the evolution of various statistics in different seasons.

- [ ] **Home Page**
  - Add welcome content by presenting the purpose of the application and evoking the highlights and statistics of the championship (winner, biggest surprise, biggest disappointment, etc.).

- [ ] **'Table' Page**
  - Improved design and layout. East and West classification added.

- [ ] **'Team Analysis' Page**
  - Addition of statistics accompanied by plot_pitch.
  - Utilize heatmaps, ... to represent team performance spatially on the pitch.

- [x] **'Team Rankings' Page**
  - Table of individual statistics to pick out the best teams for each statistic.

- [ ] **'Player Analysis' Page**
  - Graph, statistics, player comparisons, etc.

- [ ] **'Player Rankings' Page**
  - Table of individual statistics to pick out the best players for each statistic.
  - Metrics and visualizations to highlight player strengths and weaknesses.
  - Add the following functions to the table: [Stars for an overall player rating](https://dash.plotly.com/datatable/conditional-formatting#special-characters-like-emojis,-stars,-checkmarks,-circles), [Sorting](https://dash.plotly.com/datatable/interactivity), [Link to player profile](https://dash.plotly.com/dash-ag-grid/cell-renderer-components)

#### Data Preparation

- [x] Corrected the error on the overall MLS standings with FC Cincinnati and Colorado Rapids, etc.

- [x] Changed the value of “GD” for “Goal Difference” to numeric.

- [x] Scraping images of the 2023 MLS season roster from [transfermarkt](https://www.transfermarkt.com/major-league-soccer/startseite/wettbewerb/MLS1/plus/?saison_id=2022), or [mlssoccer site](https://www.mlssoccer.com/stats/players/#season=2023&competition=mls-regular-season&club=all&statType=general&position=all).

- [ ] Delete duplicate columns.

- [ ] Import data from previous seasons to improve training for future algorithms.

#### Team Analysis

- [ ] Over the years, see which stats have been the most winning for your teams.

### Future Enhancements

- [ ] Add data provided by the [itscalledsoccer](https://american-soccer-analysis.github.io/itscalledsoccer/) library from the 2023 season and integrate new functionalities into the Plotly Dash application.

- [x] Add players photo to datasets.

- [x] Statistical tracking of MLS 2023 season data projected on a [pitch](https://mplsoccer.readthedocs.io/en/latest/gallery/pitch_setup/plot_pitches.html) from the [mplsoccer](https://mplsoccer.readthedocs.io/en/latest/) library.

- [x] Import and analysis of [StatsBomb](https://statsbomb.com/) data for the Inter Miami vs Toronto FC match of the 2023 season.

- [ ] Find and Analysis of StatsBomb data with [360 data snapshots](https://statsbomb.com/what-we-do/soccer-data/360-2/) to perform advanced data analysis, as in the [video example](https://www.youtube.com/watch?v=tB_N7ei70mY).

- [ ] Add event-based analysis to get granular insights into the match.

- [ ] Salary cap calculation functionality.

- [ ] Analysis of each team's statistical weaknesses.

- [ ] Suggest players to teams according to position and profile requirements and budget.

- [ ] Recommendation system that identifies similar players based on their performance metrics.

- [ ] Match outcome prediction with historical match data to predict the outcomes of future matches.

- [ ] Analyze the oppositions of each team to understand which compositions, players or tactics are thwarting them.
