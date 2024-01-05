# Author: everyone

from django.urls import path
from .infrastructure.views.customer_views import CustomerView
from .infrastructure.views.admin_views import AdminView
from .infrastructure.views.auth_views import AuthView
from .infrastructure.views.company_views import CompanyView
from .infrastructure.views.prediction_views import PredictionView
from .infrastructure.views.market_model_views import MarketModelView
from .infrastructure.views.sentiment_model_views import SentimentModelView

urlpatterns = [
    path('admins', AdminView.as_view(({'post': 'post'}))),
    path('admins/models/trend', MarketModelView.as_view({'get': 'get_market_model_versions'}), name='models-list'),
    path('admins/models/trend-prodcution', MarketModelView.as_view({'get': 'get_market_production_model'}), name='get-production-model-id'),
    path('admins/models/trend/<str:model_version>', MarketModelView.as_view({'get': 'get_market_model_information'}), name='get-model-id'),
    path('admins/models/trend/set/<str:model_version>', MarketModelView.as_view({'post': 'update_market_model_version'}), name='train-model-id'),
    path('admins/models/trend/<str:model_version>/train',  MarketModelView.as_view({'post': 'post_market_model_version'}), name='train-model-id'),

    path('admins/models/sentiment', SentimentModelView.as_view({'get': 'get_sentiment_model_versions'}), name='models-list'),
    path('admins/models/sentiment-production', SentimentModelView.as_view({'get': 'get_sentiment_production_model'}), name='get-production-model-id'),
    path('admins/models/sentiment/<str:model_version>', SentimentModelView.as_view({'get': 'get_sentiment_model_information'}), name='get-model-id'),
    path('admins/models/sentiment/set/<str:model_version>', SentimentModelView.as_view({'post': 'update_sentiment_model_version'}), name='train-model-id'),
    path('admins/models/sentiment/<str:model_version>/train', SentimentModelView.as_view({'post': 'post_sentiment_model_version'}), name='train-model-id'),

    path('companies/history/<str:cmp>', CompanyView.as_view({'get': 'get_stock_history'}), name='company'),
    path('companies/stockTrend/<str:cmp>', CompanyView.as_view({'get': 'get_stock_trend'}), name='company'),
    path('companies/inflationTrend/', CompanyView.as_view({'get': 'get_inflation_trend'}), name='company'),
    path('companies', CompanyView.as_view({'get': 'get_all_companies'}), name='company'),
    path('companies/info/<str:cmp>', CompanyView.as_view({'get': 'get_company_info'}), name='company'),
    path('companies/testimonials/<str:cmp>', CompanyView.as_view({'get': 'get_testimonials'}), name='company'),


    path('auth/login', AuthView.as_view(({'post': 'login_user'}))),
    path("auth/logout", AuthView.as_view({'post':'logout_user'})),
    path('auth/signup', CustomerView.as_view({'post': 'create'})),

    #path('predictions', PredictionView.as_view({'get': 'get_predictions'}), name='predictions'),
    path('predictions/<str:cmp>/', PredictionView.as_view({'get': 'get_prediction'}), name='predictions'),
    path('predictions', PredictionView.as_view({'post': 'create_predictions'}), name = 'predictions'),

    path('customers/<pk>', CustomerView.as_view({'patch': 'partial_update', 'get':'retrieve', 'delete':'destroy', 'put':'update'})),
    path('customers', CustomerView.as_view({'get':'list'})),
    path('customers', CustomerView.as_view({'post': 'post'}), name='customers'),
    path('customers/<str:cid>/favorites', CustomerView.as_view({'get': 'get_favorites'}), name='customers'),
    path('customers/<str:cid>/favorites/<str:cmp>', CustomerView.as_view({'post': 'post_favorite'}), name='customers'),
    path('customers/<str:cid>/favorites/<str:cmp>/1', CustomerView.as_view({'delete': 'delete_favorite'}), name='customers'),
]