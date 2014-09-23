var storage = {
    bookmarks = [],
    support: function()
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

$(document).ready(function(e)
{
    if (storage.support())
    {
        // If localStorage is supported by client browser
        if (!localStorage['bookmarks']) localStorage['bookmarks'] = [];
        storage.bookmarks = json.parse(localStorage['bookmarks']);
        //renderBookmarkArray(storage.bookmarks)
    }



}
