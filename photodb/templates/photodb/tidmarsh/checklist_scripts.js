<script type="text/javascript">
		w = null;
		mapserver = '/'; // http://geo.salicicola.com http://172.104.19.75
		function open_tidmarsh_map(pid) {
			if (w) {
				if (! w.closed) {
					w.close();
				} 
			} 
			url = mapserver + 'tidmarsh/map/tidmarsh2/plant/all/' + pid; 
			w = open(url, 'none', 'width=920,height=810,left=5,top=5'); 
			w.focus();
			return false;
		}
		
		function open_atro_map() {
			if (w) {
				if (! w.closed) {
					w.close();
				} 
			} 
			url = "/checklists/tidmarsh/atrocinereaa_complex_map.html"; 
			w = open(url, 'none', 'width=920,height=810,left=5,top=5'); 
			w.focus();
			return false;
		}
		
		
		function open_preview_map(pid) {
				if (w) {
					if (! w.closed) {
						w.close();
					} 
				} 
				url = mapserver + '/tidmarsh/map/preview/plant/' + pid;
				w = open(url, 'none', 'width=390,height=520,top=200,left=600');  
				w.focus();
				return false;
		}
		function open_image(url) {
			if (w) {
				if (! w.closed) {
					w.close();
				} 
			} 
			w = open(url, 'none', 'width=920,height=810,left=5,top=5'); 
			w.focus();
			return false;
		}
		function open_entryform(url) {
			if (w) {
				if (! w.closed) {
					w.close();
				} 
			} 
			w = open(url, 'none', 'width=600,height=600,left=5,top=5'); 
			w.focus();
			return false;
		}			
	</script>
