from django.conf.urls import url
#from django.contrib import admin
from login import views
from django.http import HttpResponse,StreamingHttpResponse
import cv2


urlpatterns = [
	#url(r'^admin/', admin.site.urls),
	url(r'^$', views.login),
	url(r'^register/', views.register),
    url(r'^dbentry/', views.dbentry),
    url(r'^checkuser/', views.checkuser),
    url(r'^signout/', views.signout),
    url(r'^dashboard/', views.dashboard),
    url(r'^add_new_test/', views.add_new_test),
    url(r'^add_video/', views.add_video),
    url(r'^practice/', views.practice),
    url(r'^start/', views.start),
    url(r'^loading/', views.loading),
    url(r'^process/', views.process),
    url(r'^accuracy_save/', views.accuracy_save),
    
    



]
'''url(r'^start/', lambda r: StreamingHttpResponse(gen(VideoCamera()),
                                                     content_type='multipart/x-mixed-replace; boundary=frame')),'''