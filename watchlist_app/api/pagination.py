from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10


class WatchListCPagination(CursorPagination):
    page_size = 5
    
