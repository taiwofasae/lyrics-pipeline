from ingest import ingest_file, artifact, ingest_folder
from storage import file_manager
from storage import s3
from source.azlyrics import azlyrics


df, csv_list = ingest_file.main('./data/azlyrics_lyrics_n.csv')


path = artifact.create(df, './data/10-14-2014.csv')
# df1 = artifact.load(path)

# path2 = artifact.append(path, df1)
# df2 = artifact.load(path2)

# path3 = './data/10-14-2014'
# df3 = ingest_folder.main(path3, path3 + '.txt')
# print(len(df3.index))
# print(df3.tail(1))
# print(len(ingest_file.main(path3 + '.txt')[0].index))
# print(ingest_file.main(path3 + '.txt')[0].tail(1))

file_man = file_manager.File('./data/')
# path = file_man('10-14-2014.csv')
# df1 = artifact.load(path)
# print(df1.head(1))

# s3.upload_file('10-14-2014.csv', source_path=path)

taylorswift = file_man('azlyrics/taylorswift.html')
html = azlyrics._read_html_file(taylorswift)

