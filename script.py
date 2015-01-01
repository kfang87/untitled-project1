from SourceWikipedia import SourceWikipedia

source = SourceWikipedia()
uri = "http://en.wikipedia.org/w/api.php"
data = source.retrieve_data_from_source(uri)
print source.extract_relevant_context(data)