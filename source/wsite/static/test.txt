@extends('layout.layout', ['page_title' => 'Welcome to accounts!'])

@section('page')
<section class="container">
  <div style="max-width:330px;margin:100px auto 0px;">
    <h5 style="margin-bottom:25px;text-align:center;">L O G I N</h5>
    @if(Session::has('res_msg'))
    <p class="alert {{ Session::get('res_class') }}"><i class="fa fa-info-circle" aria-hidden="true"></i> {{ Session::get('res_msg') }}</p>
    @endif
    <form method="post" action="">
      @csrf
      <div class="form-group">
        <label for="username"><i class="fa fa-user" aria-hidden="true"></i> Username</label>
        <input type="text" name="_username" class="form-control" id="username" value="@if(Session::has('res_data')){{Session::get('res_data._username')}}@endif">
      </div>
      <div class="form-group">
        <label for="password"><i class="fa fa-key" aria-hidden="true"></i> Password</label>
        <input type="password" name="_password" class="form-control" id="password" value="@if(Session::has('res_data')){{Session::get('res_data._password')}}@endif">
      </div>
      <div style="margin-top:15px;">
        <button type="submit" class="btn btn-primary"><i class="fa fa-sign-in" aria-hidden="true"></i> Login</button>
      </div>
    </form>
  </div>
</section>
@stop