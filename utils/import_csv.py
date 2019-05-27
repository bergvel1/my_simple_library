import csv
import django
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# name of the CSV file to import
CSV_NAME = os.path.join(BASE_DIR, 'LIBRARY.csv')

# All column headers for the CSV, in order
FIELD_NAMES = ['BibNum', 'Title', 'Author', 'ISBN', 'PublicationYear', 'Publisher', 'Subjects', 'ItemType',
               'ItemCollection', 'FloatingItem', 'ItemLocation', 'ReportDate', 'ItemCount']

# The fields which we wish to keep
DESIRED_FIELDS = ['Title', 'Author', 'ISBN', 'Subjects']

# A dict describing the mapping of CSV field names to the fields names of the Django models
CSV_FIELDS_TO_MODEL_FIELDS = {
    'Title': 'title',
    'Author': 'author',
    'ISBN': 'isbn',
    'Subjects': 'genre'
}


def read_csv():
    """Read the csv into dictionaries, transform the keys necessary
    and return a list of cleaned-up dictionaries.
    """
    with open(CSV_NAME, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=FIELD_NAMES)
        next(reader)  # advance past the header row

        desired_cols = filter_cols(reader)

        for row in (row for row in desired_cols if
                    all(v is not (None or '') for v in [row['Title'], row['Author'], row['ISBN'], row['Subjects']])):
            yield map_rows_to_fields(row)


def filter_cols(reader):
    """
    Strip all CSV columns except for those in DESIRED_FIELDS
    :param reader: The CSV DictReader
    :return: Yields a generator for a filtered CSV reader
    """
    for row in reader:
        yield dict(zip(DESIRED_FIELDS, (row[col] for col in DESIRED_FIELDS)))


def map_rows_to_fields(row):
    """Here for each dictionary you want to transform the dictionary
    in order to map the keys of the dict to match the names of the
    fields on the model you want to create so we can pass it in as
    `**kwargs`. This would be an opportunity to use a nice dictionary
    comprehension.
    """
    return {
        CSV_FIELDS_TO_MODEL_FIELDS[key]: value for key, value in row.items()
    }


def data_well_formed(data):
    """
    Determines whether a record for a given book is formatted properly
    :param data: a dictionary representing a single book
    :return: True if the formatting is correct, false otherwise
    """

    # authors must have a first and last name
    if len(data['author']) < 2:
        return False

    # the first and last names must be nonempty
    if all(v is (None or '') for v in [data['author'][0], data['author'][1]]):
        return False

    # add more conditions here, if necessary

    return True


def clean_data(data):
    """
    Performs minor cleanup on data to make formatting easier
    :param data: uncleaned raw data
    :return: cleaned data
    """

    data['title'] = [x[0:255] for x in data['title'].split(" / ")]
    data['author'] = [x[0:255] for x in data['author'].split(", ")]
    data['isbn'] = [x[0:15] for x in data['isbn'].split(", ")]
    data['genre'] = [x[0:255] for x in data['genre'].split(", ")]

    return data


def instantiate_models():
    """Finally, we have our data from the csv in dictionaries
    that map values to expected fields on our model constructor,
    then we can just instantiate each of those models from the
    dictionary data using a list comprehension, the result of which
    we pass as the argument to `bulk_create` saving the rows to
    the database.
    """
    model_data = read_csv()

    from catalog.models import Author, Book, Genre, BookInstance

    count = 0
    for data in (data for data in model_data if data_well_formed(data)):
        data = clean_data(data)

        if count % 10 is 0:
            print("Processing row", count, data, "\n")
        count += 1

        try:
            author = (Author.objects.update_or_create(first_name=(data['author'][1]), last_name=data['author'][0]))[0]
        except IndexError:
            author = (Author.objects.update_or_create(first_name='', last_name=data['author'][0]))[0]

        genres = []
        for genre in data['genre']:
            genres.append((Genre.objects.update_or_create(name=genre))[0])

        book = (Book.objects.update_or_create(title=data['title'][0], author=author, isbn=data['isbn'][0]))[0]
        book.genre.set(genres)

        book_instance = (BookInstance.objects.update_or_create(book=book, status='a'))[0]


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_app.settings")
    django.setup()
    instantiate_models()
