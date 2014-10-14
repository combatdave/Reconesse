var storage = {
    bookmarks   : [],
    // NOTE:
    // Settings is currently not being used.
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
