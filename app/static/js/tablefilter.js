function search_on_table(tbl_id, inp_id) {
  // Declare variables 
  var input, filter, table, tbody, tr, td, i, j;
  input = document.getElementById(inp_id);
  filter = input.value.toUpperCase();
  table = document.getElementById(tbl_id);
  tbody = table.getElementsByTagName("tbody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td");
    for(j=0; j< td.length; j++){
	    if (td[j]) {
	      if (td[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
	        tr[i].style.display = "";
	        break;
	      } else {
	        tr[i].style.display = "none";
	      }
	    }
	}
  }
}