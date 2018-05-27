# CancerCellClassifier
# CellBrowser:

An app for rating cells on a scale of 1-5. The output containing the Cell-ID,Sample-ID and the rating is saved in the output directory. The app can also plot graphs when provided with the correct CSV input.



### Functionalities:

1. Plot hmmcopy from csv

2. Rate cells



## To run the app do the following steps:

### Make sure you have python 2.7.14
```python
    1.Create a conda env using: conda create --name myenv

    2.source activate myenv

    3.pip install -r requirements.txt --no-index --find-links file:///tmp/packages
```
--no-index - Ignore package index (only looking at --find-links URLs instead).

-f, --find-links <URL> - If a URL or path to an html file, then parse for links to archives. If a local path or file:// URL that's a directory, then look for archives in the directory listing.

    4.Once all the dependencies are installed you can run the app with following command: python Classifier.py

 **To rate the cells do the follwing:**

1.  Provide the percentage of cells you want to sample. example: .5


2.  Rate either using the keyboard or clicking on the button. As soon as you click the rating is saved in the output.csv file in the output directory.


And that's it!


**To add new csv:**

1. Make sure you have the correct CSV files saved in the Classifier_2 directory. The CSV files to plot must be stored in Classifier_2 directory with proper naming example: A90560A_reads.csv,A90560A_all_metrics_summary.csv,A90560A_segments.csv.


2. The library id for the csv files have to match.


3. Enter the 3 file names comma separated in the correct order. i.e **libraryid_reads.csv,libraryid_all_metrics_summary.csv,libraryid_segments.csv**


4. Press the Plot button to plot. The output will be stored in the Pdfs folder. If there are previous plots in the directory,the new ones will just be appended to the old ones.
