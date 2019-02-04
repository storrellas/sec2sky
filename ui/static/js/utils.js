class CookieMgr{

  static set(name,value,days) {
      var expires = "";
      if (days) {
          var date = new Date();
          date.setTime(date.getTime() + (days*24*60*60*1000));
          expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + (value || "")  + expires + "; path=/";
  }
  static get(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
          var c = ca[i];
          while (c.charAt(0)==' ') c = c.substring(1,c.length);
          if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
  }
  static erase(name) {
      document.cookie = name+'=; Max-Age=-99999999;';
  }

}

class JWTMgr{
  static parse(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace('-', '+').replace('_', '/');
    return JSON.parse(window.atob(base64));
  }
}

class APIMgr{
  static get_model(url, callback) {
    // Retreive companies
    const jwt_token = CookieMgr.get('jwt_token');
    $.ajax({
      type: "GET",
      url: url,
      headers: {
        "Authorization": ("Bearer " + jwt_token),
      },
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data){
        callback(data)
      },
      error: () => window.location = '/ui/',
      failure: () => window.location = '/ui/'
    })
  }

  static delete_model(url) {
    // Retreive companies
    const jwt_token = CookieMgr.get('jwt_token');
    $.ajax({
      type: "DELETE",
      url: url,
      headers: {
        "Authorization": ("Bearer " + jwt_token),
      },
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data){
        location.reload();
      },
      error: () => window.location = '/ui/',
      failure: () => window.location = '/ui/'
    })
  }




}
