from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm.query import Query
from sqlalchemy import Column, Boolean


@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    """A query compilation rule that will add limiting criteria for every
    subclass of HasPrivate"""

    if query._execution_options.get("include_private", False):
        return query

    for ent in query.column_descriptions:
        entity = ent['entity']
        if entity is None:
            continue
        insp = inspect(ent['entity'])
        mapper = getattr(insp, 'mapper', None)
        if mapper and issubclass(mapper.class_, HasPrivate):
            query = query.enable_assertions(False).filter(
                ent['entity'].public == True)

    return query


class HasPrivate(object):
    """Mixin that identifies a class as having private entities"""

    public = Column(Boolean, nullable=False)


# the recipe has a few holes in it, unfortunately, including that as given,
# it doesn't impact the JOIN added by joined eager loading.   As a guard
# against this and other potential scenarios, we can check every object as
# its loaded and refuse to continue if there's a problem
@event.listens_for(HasPrivate, "load", propagate=True)
def load(obj, context):
    if not obj.public and not \
            context.query._execution_options.get("include_private", False):
        raise TypeError(
            "private object %s was loaded, did you use "
            "joined eager loading?" % obj)
