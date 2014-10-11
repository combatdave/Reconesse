var storage = {
    bookmarks   : [],
    settings    : {},
    support     : function()
    {
        /* Check whether browser supports localStorage */
        try
        {
            return 'localStorage' in window && window['localStorage'] !== null;
        }
        catch (e)
        {
            return false;
        }
    }
}


function renderBookmark(bookmark, template, node)
{

}

function renderBookmarkArray(bookmarks, template, node)
{
    node.empty();
    for (var i = 0; i < bookmarks.length; ++i)
    {
        renderBookmark(bookmarks[i],
                       template,
                       node)
    }
}


function bookmarkPerson(data)
{
    // If not exists in bookmark array
}

