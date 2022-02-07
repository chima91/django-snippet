from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from snippets.models import Snippet
from snippets.forms import SnippetForm


def top(request):
  snippets = Snippet.objects.all()  # スニペットの一覧を取得
  context = {"snippets": snippets}  # テンプレートエンジンに与えるPythonオブジェクト
  return render(request, "snippets/top.html", context)


@login_required
def snippet_new(request):
  if request.method == 'POST':
    form = SnippetForm(request.POST)
    if form.is_valid():
      snippet = form.save(commit=False)
      snippet.created_by = request.user
      snippet.save()
      return redirect(snippet_detail, snippet_id=snippet.pk)
  else:
    form = SnippetForm()
  context = {'form': form}
  return render(request, "snippets/snippet_new.html", context)

@login_required
def snippet_edit(request, snippet_id):
  snippet = get_object_or_404(Snippet, pk=snippet_id)
  if snippet.created_by_id != request.user.id:
    return HttpResponseForbidden("このスニペットの編集は許可されていません。")
  if request.method == "POST":
    form = SnippetForm(request.POST, instance=snippet)
    if form.is_valid():
      form.save()
      return redirect('snippet_detail', snippet_id=snippet.id)
  else:
    form = SnippetForm(instance=snippet)
  context = {'form': form}
  return render(request, "snippets/snippet_edit.html", context)

def snippet_detail(request, snippet_id):
  snippet = get_object_or_404(Snippet, pk=snippet_id)
  context = {'snippet': snippet}
  return render(request, 'snippets/snippet_detail.html', context)