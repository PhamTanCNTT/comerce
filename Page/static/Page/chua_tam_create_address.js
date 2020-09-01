//ajax create address
            //create nation
            // var url_nation = "/connectdata/NationProView/84/";
            function create_address_nation() {
                $.getJSON(url_nation,{},create_address_nation1);
            }
            function create_address_nation1(nation) {
                var z = document.createElement("option");
                    z.setAttribute("id", "option_nation");
                    z.setAttribute("value", nation.id);
                    // z.onchange = change_address_nation();
                    var t = document.createTextNode(nation.name);
                    z.appendChild(t);
                    document.getElementById("Select_Nation").appendChild(z);
            }

            window.onload = create_address_nation();

            //create province
            // var url_address_province = "/connectdata/ProDisView/";
            function create_province() {
                $.getJSON(url_get_id_profile,{},create_province1);
            }
            function create_province1(profile) {
                $.getJSON(url_address_province + parseInt(profile[0].address[0].Province) + "/",{},create_province2);
            }
            function create_province2(province) {
                 var z = document.createElement("option");
                    z.setAttribute("id", "option_province");
                    z.setAttribute("value", province.id);
                    // z.onchange = change_address_district(province.id);
                    var t = document.createTextNode(province.name);
                    z.appendChild(t);
                    document.getElementById("Select_Province").appendChild(z);
            }
            window.onload = create_province();

            //create District
            var url_address_district = "/connectdata/DisWardView/";
            function create_district() {
                $.getJSON(url_get_id_profile,{},create_district1);
            }
            function create_district1(profile) {
                $.getJSON(url_address_district + parseInt(profile[0].address[0].District) + "/",{},create_district2);
            }
            function create_district2(district) {
                 var z = document.createElement("option");
                    z.setAttribute("id", "option_district");
                    z.setAttribute("value", district.id);
                    var t = document.createTextNode(district.name);
                    z.appendChild(t);
                    document.getElementById("Select_District").appendChild(z);
            }
            window.onload = create_district();

            //create ward
            var url_address_ward = "/connectdata/WardView/";
            function create_ward() {
                $.getJSON(url_get_id_profile,{},create_ward1);
            }
            function create_ward1(profile) {
                $.getJSON(url_address_ward + profile[0].address[0].Ward + "/",{},create_ward2);
            }
            function create_ward2(ward) {
                 var z = document.createElement("option");
                    z.setAttribute("id", "option_ward");
                    z.setAttribute("value", ward.id);
                    var t = document.createTextNode(ward.name);
                    z.appendChild(t);
                    document.getElementById("Select_Ward").appendChild(z);
            }
            window.onload = create_ward();
            // end ajax create address


            // ajax change address
            $(document).ready(function() {
                $('#Select_Nation').onchange(change_address_province());
            });

            function change_address_province(){
                $.getJSON(url_nation,{},change_address_province1);
            }

            function change_address_province1(nation){
                for (var i = 0; i < nation.province.length; i++){
                    var x = document.createElement("option")
                        x.setAttribute("id", "option_province")
                        x.setAttribute("value", nation.province[i].id)
                        // x.onchange = change_address_district();
                        var y = document.createTextNode(nation.province[i].name);
                        x.appendChild(y);
                        document.getElementById("Select_Province").appendChild(x);
                }
            }
            //end ajax change address