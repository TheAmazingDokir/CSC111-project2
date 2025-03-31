import plotly.express as px
import class_graph as cg
import stats


def render_scatter(webgraph: cg.Webgraph) -> None:

    name = lambda v: (f"Website: {v.domain_name}<br>"+
                        f"Avg Daily Min: {v.stats['daily_min']} ({stats.percentify(v.stats['daily_min'], stats.calc_global_daily_min, webgraph)}% global)<br>"+
                        f"Daily Unique Pageviews: {v.stats['daily_pageviews']} ({stats.percentify(v.stats['daily_pageviews'], stats.calc_global_daily_pageviews, webgraph)}% global)<br>"+
                        f"Avg Min Per Page: {v.stats['min_per_page']} ({stats.percentify(v.stats['min_per_page'], stats.calc_global_min_per_page, webgraph)}% global)<br>"+
                        f"Search Traffic Impact: {v.stats['search_traffic']}% ({stats.percentify(v.stats['search_traffic'], stats.calc_global_search_traffic, webgraph)}% global)<br>"+
                        f"Total Sites Linking-in: {v.stats['site_links']} ({stats.percentify(v.stats['site_links'], stats.calc_global_site_links, webgraph)}% global)<br>"+
                        f"Links Traffic Impact: {v.stats['links_traffic']}% ({stats.percentify(v.stats['links_traffic'], stats.calc_global_links_traffic, webgraph)}% global)<br>"+
                        f"Engagement Rating: {v.stats['engagement_rating']} ({stats.percentify(v.stats['engagement_rating'], stats.calc_global_engagement_rating, webgraph)}% global)<br>"+
                        f"Predicted Rank: {v.stats['predicted_rank']}")

    x = [len(v.links_in) for v in webgraph.get_vertices()]
    y = [v.stats["engagement_rating"] for v in webgraph.get_vertices()]
    fig = px.scatter(x=x ,y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
    fig.update_layout(xaxis_title="Number of Sites Linking-in", yaxis_title="Engagement Rating")
    fig.show()

    x = [len(v.links_out) for v in webgraph.get_vertices()]
    y = [v.stats["engagement_rating"] for v in webgraph.get_vertices()]
    fig = px.scatter(x=x ,y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
    fig.update_layout(xaxis_title="Number of Outgoing Links", yaxis_title="Engagement Rating")
    fig.show()

    x = [v.stats["links_traffic"] for v in webgraph.get_vertices()]
    y = [v.stats["engagement_rating"] for v in webgraph.get_vertices()]
    fig = px.scatter(x=x ,y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
    fig.update_layout(xaxis_title="Links Traffic Impact", yaxis_title="Engagement Rating")
    fig.show()
    
    x = [v.stats["search_traffic"] for v in webgraph.get_vertices()]
    y = [v.stats["engagement_rating"] for v in webgraph.get_vertices()]
    fig = px.scatter(x=x ,y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
    fig.update_layout(xaxis_title="Search Traffic Impact", yaxis_title="Engagement Rating")
    fig.show()