from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from read_app.forms.teachers import TeacherRegistrationForm
from read_app.models import User, Student, ClassSection, ArchivedStudent
import datetime


