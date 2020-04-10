from googleapiclient.discovery import build

import environment as env

################################################################################################

# Function for google search accepting search keyword as input and returning max allowed search result
def google_search(search_term, **kwargs):

    service = build("customsearch", "v1", developerKey=env.GOOGLE_SEARCH_API_KEY)

    results = service.cse().list(
        q=search_term,
        cx=env.GOOGLE_SEARCH_ENGINE_ID,
        **kwargs,
    ).execute()

    results_list = results.get('items', [])

    # create search results from the above and return formatted search results
    search_result = []
    for result in results_list[:env.MAX_SEARCH_RESULT_COUNT]:
        search_result.append({
            'title': result.get('title'),
            'link': result.get('link'),
            'description': result.get('snippet')
        })
        
    return search_result

################################################################################################