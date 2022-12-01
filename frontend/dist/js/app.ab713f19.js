(function(){var e={7411:function(e,t,s){"use strict";var a=s(6369),o=function(){var e=this,t=e._self._c;return t("v-app",[e.mainStore.isLoggedIn?t("v-navigation-drawer",{attrs:{clipped:e.$vuetify.breakpoint.lgAndUp,app:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[t("v-list",{attrs:{dense:""}},[e._l(e.menus,(function(s){return[s.children?t("v-list-group",{key:s.text,attrs:{"prepend-icon":s.icon,"append-icon":s["icon-alt"]},scopedSlots:e._u([{key:"activator",fn:function(){return[t("v-list-item-content",[t("v-list-item-title",[e._v(" "+e._s(s.text)+" ")])],1)]},proxy:!0}],null,!0)},e._l(s.children,(function(s,a){return t("v-list-item",{key:a,attrs:{to:{name:s.route}}},[s.icon?t("v-list-item-action",[t("v-icon",[e._v(e._s(s.icon))])],1):e._e(),t("v-list-item-content",[t("v-list-item-title",[e._v(" "+e._s(s.text)+" ")])],1)],1)})),1):t("v-list-item",{key:s.text,attrs:{to:{name:s.route}}},[t("v-list-item-action",[t("v-icon",[e._v(e._s(s.icon))])],1),t("v-list-item-content",[t("v-list-item-title",[e._v(" "+e._s(s.text)+" ")])],1)],1)]}))],2)],1):e._e(),t("v-app-bar",{attrs:{"clipped-left":e.$vuetify.breakpoint.lgAndUp,color:"#00F5FF",app:""}},[e.mainStore.isLoggedIn?t("v-app-bar-nav-icon",{on:{click:function(t){t.stopPropagation(),e.drawer=!e.drawer}}}):e._e(),t("v-spacer"),e.mainStore.isLoggedIn?t("v-toolbar-items",[t("LocaleSwitcher"),t("v-btn",{attrs:{text:""}},[e._v(e._s(e.mainStore.logged_user.name))]),t("v-btn",{attrs:{icon:""},on:{click:e.mainStore.logout}},[t("v-icon",[e._v("mdi-logout")])],1)],1):t("v-toolbar-items",[t("LocaleSwitcher")],1)],1),t("header",[t("link",{attrs:{href:"https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900",rel:"stylesheet"}}),t("link",{attrs:{href:"https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css",rel:"stylesheet"}})]),t("v-main",[t("vue-particles",{attrs:{color:"#7afff6"}}),t("flash-message",{staticStyle:{height:"5px"}}),t("router-view"),t("loader")],1),t("v-footer",{attrs:{app:""}})],1)},r=[],n=s(3556),i=s(6265),l=s.n(i),c=s(1598),d=s(6018),u=s(8308),m=s(6808);function _(e){return e["en"]["$vuetify"]=u.Z,e["es"]["$vuetify"]=m.Z,e}function h(){const e=s(8092);let t={};return e.keys().forEach((s=>{const a=s.match(/([A-Za-z0-9-_]+)\./i);if(a&&a.length>1){const o=a[1];t[o]=e(s)}})),t=_(t),t}a["default"].use(d.Z);const p=new d.Z({locale:"es",fallbackLocale:"es",messages:h()}),f={id:"",name:"",email:"",role:""},v=(0,n.Q_)("main",{state:()=>({token:localStorage.getItem("access_token")||"",logged_user:f,employees:[],cycles:[],networks:[],areas:[],network_modes:[],loader:!1,flash_message:"",flash_message_type:""}),getters:{isLoggedIn:e=>!!e.token},actions:{async initialize(){this.getAreas(),this.getEmployees(),this.getNetworks(),this.getCycles()},async logIn(e){await l().post("https://oahub.finacanalytics.com/api/v1/login",e).then((e=>{let t=e.data.token;localStorage.setItem("access_token",t),this.token=t,this.setLoggedUser(),this.initialize(),this.router.push("/home").catch((e=>{console.log(e)}))})).catch((e=>{console.log(e),this.$reset(),localStorage.removeItem("access_token"),this.setFlashMessage({message:e.response.data,type:"error"}),this.router.push("/login").catch((()=>{}))}))},logout(){this.$reset(),localStorage.removeItem("access_token"),this.logged_user=f,this.token="",this.router.push("/login").catch((()=>{}))},setLoggedUser(){let e=(0,c.Z)(this.token);this.logged_user.id=e.id,this.logged_user.name=e.username,this.logged_user.email=e.email,this.logged_user.role=e.roles[0].name},async getNetworkModes(e){if(e){const t=await l().get("https://oahub.finacanalytics.com/api/v1/cycle/"+e+"/network_modes");this.network_modes=t.data}},async getEmployees(){const e=await l().get("https://oahub.finacanalytics.com/api/v1/users");this.employees=e.data},async getCycles(){const e=await l().get("https://oahub.finacanalytics.com/api/v1/cycles");this.cycles=e.data},async getNetworks(){const e=await l().get("https://oahub.finacanalytics.com/api/v1/networks/"+p.locale);this.networks=e.data},async getAreas(){const e=await l().get("https://oahub.finacanalytics.com/api/v1/areas");this.areas=e.data},setFlashMessage(e){e.message?(this.flash_message=p.t(`${e.message}`),this.flash_message_type=e.type):(this.flash_message="",this.flash_message_type=null)}}});var g=function(){var e=this,t=e._self._c;return t("v-menu",{attrs:{bottom:"",left:""},scopedSlots:e._u([{key:"activator",fn:function({on:s,attrs:a}){return[t("v-btn",e._g(e._b({attrs:{icon:""}},"v-btn",a,!1),s),[t("v-icon",[e._v("mdi-web")]),e._v(e._s(e.$i18n.locale)+" ")],1)]}}])},[t("v-list",e._l(e.filteredLocales,(function(s){return t("v-list-item",{key:s},[t("v-list-item-title",{on:{click:function(t){return e.switchLocale(s)}}},[e._v(e._s(s.toUpperCase()))])],1)})),1)],1)},w=[],k={name:"LocaleSwitcher",data(){return{locales:"es,en".split(",")}},computed:{filteredLocales(){return this.locales.filter((e=>e!==this.$i18n.locale))}},methods:{switchLocale(e){this.$i18n.locale!==e&&(this.$i18n.locale=e)}}},y=k,b=s(1001),x=(0,b.Z)(y,g,w,!1,null,null,null),$=x.exports,C=function(){var e=this,t=e._self._c;return t("div",{staticClass:"text-xs-center"},[t("v-dialog",{attrs:{"hide-overlay":"",persistent:"",width:"300"},model:{value:e.loader,callback:function(t){e.loader=t},expression:"loader"}},[t("v-card",{attrs:{color:"primary",dark:""}},[t("v-card-text",[e._v(" "+e._s(e.$t("menus.loading"))+" "),t("v-progress-linear",{staticClass:"mb-0",attrs:{indeterminate:"",color:"white"}})],1)],1)],1)],1)},q=[],S={computed:{...(0,n.rn)(v,["loader"])}},A=S,E=(0,b.Z)(A,C,q,!1,null,null,null),N=E.exports,L=function(){var e=this,t=e._self._c;return t("div",[t("v-row",[t("v-col",{attrs:{md:"6","offset-md":"3"}},[e.flash_message?t("v-alert",{attrs:{type:e.flash_message_type,text:"",dismissible:""},on:{input:e.onClose}},[e._v(" "+e._s(e.flash_message)+" ")]):e._e()],1)],1)],1)},O=[],j={computed:{...(0,n.rn)(v,["flash_message","flash_message_type"])},watch:{flash_message(e){e&&setTimeout((()=>{this.setFlashMessage({})}),5e3)}},methods:{...(0,n.nv)(v,["setFlashMessage"]),onClose(){this.setFlashMessage({})}}},T=j,I=(0,b.Z)(T,L,O,!1,null,null,null),M=I.exports,P={data(){return{drawer:!0,menus:[{icon:"mdi-list",text:this.$t("menus.active_source"),route:"Home",roles:["Admin"]},{icon:"mdi-account_balance",text:this.$t("menus.culture"),route:"About",roles:["Admin"]}]}},components:{LocaleSwitcher:$,Loader:N,flashMessage:M},created(){this.mainStore.isLoggedIn&&(this.mainStore.initialize(),this.mainStore.setLoggedUser()),this.$axios.interceptors.request.use((e=>(this.mainStore.loader=!0,e)),(e=>(this.mainStore.loader=!1,Promise.reject(e)))),this.$axios.interceptors.response.use((e=>(this.mainStore.loader=!1,e)),(e=>(this.mainStore.loader=!1,Promise.reject(e))))},mounted(){},computed:{...(0,n.Kc)(v)},watch:{"$i18n.locale"(){this.translateMenus()}},methods:{translateMenus(){this.menus[0].text=this.$t("menus.active_source"),this.menus[1].text=this.$t("menus.culture")}}},F=P,H=(0,b.Z)(F,o,r,!1,null,"581ab35d",null),U=H.exports,Z=s(2631),R=function(){var e=this,t=e._self._c;return t("v-container",{attrs:{fluid:""}},[t("v-row",{attrs:{dense:""}},[t("v-col",{staticClass:"d-flex justify-space-around mb-6 align-end",attrs:{cols:"3"}},[t("v-select",{attrs:{items:e.filteredCycles,label:e.$t("main_page.period"),"item-text":"Cycle","item-value":"id_cycle",clearable:""},on:{change:e.initialize,"click:clear":e.resetSelectedVariables},model:{value:e.selected_cycle,callback:function(t){e.selected_cycle=t},expression:"selected_cycle"}})],1),t("v-col",{staticClass:"d-flex justify-space-around mb-6 align-end",attrs:{cols:"3"}},[t("v-select",{attrs:{items:e.mainStore.networks,label:e.$t("main_page.questionaire_type"),"item-text":`name_${e.$i18n.locale}`,"item-value":"id",clearable:"","return-object":""},on:{"click:clear":e.clearVariables,change:e.getQuestions},model:{value:e.selected_network,callback:function(t){e.selected_network=t},expression:"selected_network"}})],1),e.filteredNetwokModeThemes?t("v-col",{staticClass:"d-flex justify-space-around mb-6 align-end",attrs:{cols:"3"}},[t("v-select",{attrs:{items:e.filteredNetwokModeThemes,label:e.$t("main_page.question_theme"),"item-text":`Network_mode_theme_${e.$i18n.locale}`,"item-value":"id_network_mode_theme",clearable:""},on:{change:e.getQuestions,"click:clear":e.clearVariables},model:{value:e.selected_network_mode_theme,callback:function(t){e.selected_network_mode_theme=t},expression:"selected_network_mode_theme"}})],1):e._e()],1),e.selected_network&&"actor"===e.selected_network.code?t("v-row",[t("v-col",{staticClass:"d-flex justify-space-around mb-6 align-end",attrs:{cols:"3"}},[t("v-select",{attrs:{items:e.mainStore.areas,label:e.$t("main_page.area"),"item-text":`Organization_area_${e.$i18n.locale}`,"item-value":"id_organization_area",clearable:""},model:{value:e.selected_area,callback:function(t){e.selected_area=t},expression:"selected_area"}})],1),t("v-col",{staticClass:"d-flex justify-space-around mb-6 align-end",attrs:{cols:"3"}},[t("v-autocomplete",{attrs:{items:e.filteredEmployees,"item-text":"username","item-value":"id",label:e.$t("main_page.user"),"persistent-hint":"",dense:"","small-chips":"",multiple:"","return-object":""},on:{change:function(t){return e.addInteractingActor()}},model:{value:e.selected_actors,callback:function(t){e.selected_actors=t},expression:"selected_actors"}})],1)],1):e._e(),t("v-row",{attrs:{dense:"",justify:"space-around"}},[t("v-col",{attrs:{cols:"3"}},e._l(e.questions,(function(s,a){return t("div",{key:a},[t("v-card",[t("v-app-bar",{attrs:{flat:"",color:"blue"}},[t("v-card-title",{staticClass:"white--text"},[e._v(" "+e._s(e.$t("main_page.question"))+" "+e._s(a+1)+" ")])],1),t("v-card-text",[e._v(e._s(s[`Question_${e.$i18n.locale}`]))])],1),t("br")],1)})),0),e.selected_network&&"actor"===e.selected_network.code?t("v-col",{attrs:{cols:"9"}},[e.selected_actors.length>0?t("v-data-table",{staticClass:"elevation-1",attrs:{headers:e.tableActorsHeader,items:e.selected_actors,"items-per-page":-1},scopedSlots:e._u([{key:"item",fn:function({item:s}){return[t("tr",[t("td",{staticClass:"text-xs-left"},[e._v(e._s(s.username))]),t("td",{staticClass:"text-xs-left"},[e._v(e._s(s.organization_area[`Organization_area_${e.$i18n.locale}`]))]),e._l(e.questions,(function(a,o){return t("td",{key:o},[t("v-select",{staticClass:"my-5",attrs:{id:`sel_${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id}`,items:JSON.parse(a.question_possible_answers[`Question_possible_answers_${e.$i18n.locale}`]),"item-text":"texto","item-value":"valor",clearable:"",multiple:a.question_possible_answers.multiple,"deletable-chips":"","small-chips":"",outlined:"",flat:"",rounded:""},on:{change:function(t){return e.saveAnswersArray(t,s.id,a.id_question)}},model:{value:e.answers[`${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id}`],callback:function(t){e.$set(e.answers,`${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id}`,t)},expression:"answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`]"}})],1)})),t("td",[t("v-tooltip",{attrs:{bottom:""},scopedSlots:e._u([{key:"activator",fn:function({on:a}){return[t("v-icon",e._g({attrs:{small:"",color:"orange"},on:{click:function(t){return e.delRecord(s)}}},a),[e._v(" mdi-delete ")])]}}],null,!0)},[t("span",[e._v("Borrar")])])],1)],2)]}}],null,!1,1041055654)}):e._e()],1):e._e(),e.selected_network&&"actor"!==e.selected_network.code?t("v-col",{attrs:{cols:"9"}},[e.nodes?t("v-data-table",{staticClass:"elevation-1",attrs:{headers:e.tableNodesHeader,items:e.nodes,"items-per-page":-1},scopedSlots:e._u([{key:"item",fn:function({item:s}){return[t("tr",[t("td",{staticClass:"text-xs-left"},[e._v(e._s(s[`Node_${e.$i18n.locale}`]))]),e._l(e.questions,(function(a,o){return t("td",{key:o},[t("v-select",{staticClass:"my-5",attrs:{id:`sel_${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id_node}`,items:JSON.parse(a.question_possible_answers[`Question_possible_answers_${e.$i18n.locale}`]),"item-text":"texto","item-value":"valor",clearable:"",multiple:a.question_possible_answers.multiple,"deletable-chips":"","small-chips":"",outlined:"",flat:"",rounded:""},on:{change:function(t){return e.saveAnswersArray(t,s.id_node,a.id_question)}},model:{value:e.answers[`${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id_node}`],callback:function(t){e.$set(e.answers,`${e.current_network_mode.id_network_mode}_${a.id_question}_${s.id_node}`,t)},expression:"answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id_node}`]"}})],1)}))],2)]}}],null,!1,1188396378)}):e._e()],1):e._e()],1),t("confirmation-dialog",{ref:"confirmDeleteActor"})],1)},z=[],Q=function(){var e=this,t=e._self._c;return t("v-dialog",{style:{zIndex:e.options.zIndex},attrs:{"max-width":e.options.width},on:{keydown:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"esc",27,t.key,["Esc","Escape"])?null:e.cancel.apply(null,arguments)}},model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[t("v-card",[t("v-toolbar",{attrs:{dark:"",color:e.options.color,dense:"",flat:""}},[t("v-toolbar-title",{staticClass:"text-body-2 font-weight-bold black--text"},[e._v(" "+e._s(e.title)+" ")])],1),t("v-card-text",{directives:[{name:"show",rawName:"v-show",value:!!e.message,expression:"!!message"}],staticClass:"pa-4 black--text",domProps:{innerHTML:e._s(e.message)}}),t("v-card-actions",{staticClass:"pt-3"},[t("v-spacer"),e.options.noconfirm?e._e():t("v-btn",{staticClass:"body-2 font-weight-bold",attrs:{color:"grey",text:""},nativeOn:{click:function(t){return e.cancel.apply(null,arguments)}}},[e._v(e._s(e.$t("menus.cancel")))]),t("v-btn",{staticClass:"body-2 font-weight-bold",attrs:{color:"primary",outlined:""},nativeOn:{click:function(t){return e.agree.apply(null,arguments)}}},[e._v("OK")])],1)],1)],1)},B=[],D={name:"ConfirmDlg",data(){return{dialog:!1,resolve:null,reject:null,message:null,title:null,options:{color:"grey lighten-3",width:400,zIndex:200,noconfirm:!1}}},methods:{open(e,t,s){return this.dialog=!0,this.title=e,this.message=t,this.options=Object.assign(this.options,s),new Promise(((e,t)=>{this.resolve=e,this.reject=t}))},agree(){this.resolve(!0),this.dialog=!1},cancel(){this.resolve(!1),this.dialog=!1}}},V=D,J=(0,b.Z)(V,Q,B,!1,null,null,null),K=J.exports,W={components:{ConfirmationDialog:K},data(){return{selected_actors:[],selected_cycle:null,selected_network:null,selected_area:null,selected_node_segment_category:null,selected_network_mode_theme:null,questions:[],answers:{},nodes:[],current_network_mode:null,selRules:[e=>e&&e.length<=2||"Máximo 2 opciones!! ${v.length}"],defaultActorsHeader:[{text:"Nombre",align:"start",value:"username",class:"white--text"},{text:"Area",value:"id_organization_area",class:"white--text"},{text:"Acciones",class:"white--text",sortable:!1}],defaultNodesHeader:[{text:"Nombre",align:"start",value:"name",class:"white--text"}]}},computed:{interactingPeopleIds(){return this.selected_actors?this.selected_actors.map((e=>e.id)):[]},filteredCycles(){return this.mainStore.cycles.filter((e=>e.Is_active))},filteredEmployees(){return this.selected_area?this.mainStore.employees.filter((e=>e.id_organization_area===this.selected_area)):null},filteredNetwokModeThemes(){if(this.selected_network){let e=this.mainStore.network_modes.filter((e=>e.id_network===this.selected_network.id&&e.network_mode_theme));return e&&e.length?e.map((e=>e.network_mode_theme)):null}return null},tableActorsHeader(){return this.makeActorsTableHeader(this.questions,this.defaultActorsHeader,this.$t("main_page.question"))},tableNodesHeader(){return this.makeNodesTableHeader(this.questions,this.defaultNodesHeader,this.$t("main_page.question"))},...(0,n.Kc)(v)},methods:{saveAnswersArray(e,t,s){console.log("Entra a SaveAnswerArray"),console.log(e),this.$set(this.answers,`${this.current_network_mode.id_network_mode}_${s}_${t}`,e);const a={cycle_id:this.selected_cycle,user_email:this.mainStore.logged_user.email,item_id:t,question_id:s,network_mode_id:this.current_network_mode.id_network_mode,selected_option:e};this.$axios.post("https://oahub.finacanalytics.com/api/v1/save_answer",a).then((e=>{this.$alertify.success(this.$t(e.data))})).catch((e=>{this.$alertify.error(this.$t(e.message)),console.error("There was an error!",e.message)}))},makeActorsTableHeader(e,t,s){let a=Object.assign([],t);return e&&e.length>0&&e.forEach(((e,t)=>{a.splice(2+t,0,{text:`${s} ${t+1}`,align:"center",class:"white--text",sortable:!1})})),a[0].text=this.$t("main_page.actor_table.name"),a[1].text=this.$t("main_page.actor_table.area"),a[a.length-1].text=this.$t("main_page.actor_table.actions"),a},makeNodesTableHeader(e,t,s){let a=Object.assign([],t);return e&&e.length>0&&e.forEach(((e,t)=>{a.splice(1+t,0,{text:`${s} ${t+1}`,align:"center",class:"white--text",sortable:!1})})),a[0].text=this.selected_network[`name_${this.$i18n.locale}`],a},sortSelectedColleagues(){this.selected_actors.sort(((e,t)=>e.username.toLowerCase()<t.username.toLowerCase()?-1:t.username.toLowerCase()>e.username.toLowerCase()?1:0))},async addInteractingActor(){const e={user_email:this.mainStore.logged_user.email,employee_ids:this.interactingPeopleIds,cycle_id:this.selected_cycle};await this.$axios.post("https://oahub.finacanalytics.com/api/v1/add_interacting_actor",e).then((e=>console.log(e.data))).catch((e=>{console.error("There was an error!",e.message)})),this.sortSelectedColleagues()},async delRecord(e){await this.$refs.confirmDeleteActor.open(this.$t("menus.delete_record_title"),this.$t("menus.delete_record_text"),{color:"red lighten-3"})&&await this.deleteActor(e)},async deleteActor(e){let t=this.selected_actors.findIndex((t=>t.id==e.id));const s={user_email:this.mainStore.logged_user.email,item_id:e.id,cycle_id:this.selected_cycle};await this.$axios.delete("https://oahub.finacanalytics.com/api/v1/delete_interacting_actor",{data:s}).then((e=>{console.log(e.data),this.selected_actors.splice(t,1)})).catch((e=>{console.error("There was an error!",e.message)}))},resetSelectedVariables(){this.selected_area=null,this.selected_cycle=null,this.selected_actors=null,this.selected_network=null,this.selected_node_segment_category=null,this.selected_network_mode_theme=null,this.questions=[],this.nodes=[],this.current_network_mode=null,this.answers=[]},clearVariables(){this.questions=[],this.selected_network_mode_theme=null,this.current_network_mode=null,this.nodes=[]},async getNodes(e){const t=await this.$axios.get("https://oahub.finacanalytics.com/api/v1/network_mode/"+e+"/nodes");this.nodes=t.data},async getActors(){await this.$axios.get("https://oahub.finacanalytics.com/api/v1/user/"+this.mainStore.logged_user.id+"/cycle/"+this.selected_cycle+"/interacting_actors").then((e=>{const t=e.data;this.selected_actors=this.mainStore.employees.filter((e=>t.includes(e.id)))})).catch((e=>{console.error("There was an error!",e.message)}))},async getUserResponses(){await this.$axios.get("https://oahub.finacanalytics.com/api/v1/user/"+this.mainStore.logged_user.id+"/cycle/"+this.selected_cycle+"/responses").then((e=>{const t=e.data;t&&t.forEach((e=>{const t=JSON.parse(e.Response);t.forEach((t=>{this.answers[`${e.adjacency_input_form["id_network_mode"]}_${e.id_question}_${t.item_id}`]=t.valor}))}))})).catch((e=>{console.error("There was an error!",e.message)}))},async getNetworkModeQuestions(e){if(e){const t=await this.$axios.get("https://oahub.finacanalytics.com/api/v1/network_mode/"+e+"/questions");this.questions=t.data}},async getQuestions(){this.questions=[],this.selected_network&&"actor"===this.selected_network.code&&this.filteredNetwokModeThemes?this.selected_network_mode_theme&&(this.current_network_mode=this.mainStore.network_modes.filter((e=>e.id_network===this.selected_network.id&&e.id_network_mode_theme===this.selected_network_mode_theme))[0]):this.selected_network&&"actor"!==this.selected_network.code&&(this.current_network_mode=this.mainStore.network_modes.filter((e=>e.id_network===this.selected_network.id))[0],await this.getNodes(this.current_network_mode.id_network_mode)),this.current_network_mode&&this.getNetworkModeQuestions(this.current_network_mode.id_network_mode)},async initialize(){this.selected_cycle&&(await this.getActors(),await this.mainStore.getNetworkModes(this.selected_cycle),await this.getUserResponses())}}},X=W,Y=(0,b.Z)(X,R,z,!1,null,null,null),G=Y.exports,ee=function(){var e=this,t=e._self._c;return t("v-container",{attrs:{"fill-height":"",fluid:""}},[t("v-layout",{attrs:{"align-center":"","justify-center":""}},[t("v-flex",{attrs:{xs12:"",sm8:"",md4:""}},[t("v-card",{staticClass:"elevation-12"},[t("v-img",{attrs:{height:"250px",src:"images/OA-HUB-cropped.png"}},[t("v-app-bar",{attrs:{flat:"",color:"rgba(0, 0, 0, 0)"}})],1),t("v-card-text",[t("v-form",[t("v-text-field",{attrs:{"prepend-icon":"mdi-email",label:"Email",type:"text",rules:[t=>!!t||e.$t("login.email_required"),t=>/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(t)||e.$t("login.email_not_valid")]},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),t("v-text-field",{attrs:{id:"password","prepend-icon":"mdi-lock",label:e.$t("login.password"),type:e.show?"text":"password","append-icon":e.show?"mdi-eye":"mdi-eye-off",rules:[t=>!!t||e.$t("login.pwd_required"),t=>/^\w(?=.{4,})/.test(t)||e.$t("login.min_pwd")]},on:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.logIn.apply(null,arguments)},"click:append":function(t){e.show=!e.show}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),t("a",{attrs:{href:e.forgotURL}},[e._v(e._s(e.$t("login.forgot_pwd")))])],1)],1),t("v-card-actions",[t("v-spacer"),t("v-btn",{attrs:{color:"primary"},on:{click:e.logIn}},[e._v("Login")])],1)],1)],1)],1)],1)},te=[],se={data(){return{email:null,password:null,show:!1,forgotURL:window.location.origin+"/forgot-password"}},computed:{...(0,n.Kc)(v)},methods:{async logIn(){let e={email:this.email,password:this.password};this.mainStore.logIn(e)}}},ae=se,oe=(0,b.Z)(ae,ee,te,!1,null,null,null),re=oe.exports,ne=function(){var e=this,t=e._self._c;return t("v-app",{attrs:{id:"inspire"}},[t("v-main",[t("v-row",{staticClass:"back-top"}),t("v-container",{attrs:{fluid:""}},[t("v-row",[t("v-layout",{attrs:{"align-center":"","justify-center":""}},[t("v-flex",{attrs:{xs12:"",sm8:"",md4:""}},[t("v-card",{staticClass:"elevation-12"},[t("v-toolbar",{attrs:{dark:"",color:"primary"}},[t("v-toolbar-title",[e._v("Restablecer contraseña...")]),t("v-spacer")],1),t("v-card-text",[t("v-form",{model:{value:e.valid_form,callback:function(t){e.valid_form=t},expression:"valid_form"}},[t("v-text-field",{attrs:{"prepend-icon":"mdi-email",label:"Email",type:"text",rules:[e=>!!e||"E-mail es requerido!",e=>/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(e)||"E-mail no es válido"]},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}})],1)],1),t("v-card-actions",[t("v-spacer"),t("v-btn",{attrs:{color:"primary"},on:{click:e.cancel}},[e._v("Cancelar")]),t("v-btn",{attrs:{color:"primary",disabled:e.isValidForm},on:{click:e.requestResetPassword}},[e._v("Enviar solicitud")])],1)],1)],1)],1)],1)],1)],1)],1)},ie=[],le={data(){return{email:null,has_error:!1,valid_form:!1}},computed:{isValidForm(){return!this.valid_form}},methods:{cancel(){this.$router.push({path:"Login"})},requestResetPassword(){this.$axios.post("api/forgot-password",{email:this.email}).then((e=>{console.log(e),this.setFlashMessage({message:"Un correo ha sido enviado a su cuenta para restablecer su contraseña: "+this.email,type:"success"}),this.$router.replace("/")})).catch((e=>{console.log(e),this.setFlashMessage({message:"No existe la dirección de correo: "+this.email,type:"error"}),this.email=""}))}}},ce=le,de=(0,b.Z)(ce,ne,ie,!1,null,null,null),ue=de.exports,me=function(){var e=this,t=e._self._c;return t("v-app",{attrs:{id:"inspire"}},[t("v-main",[t("v-row",{staticClass:"back-top"}),t("v-container",{attrs:{fluid:""}},[t("v-row",[t("v-layout",{attrs:{"align-center":"","justify-center":""}},[t("v-flex",{attrs:{xs12:"",sm8:"",md4:""}},[t("v-card",{staticClass:"elevation-12"},[t("v-toolbar",{attrs:{dark:"",color:"primary"}},[t("v-toolbar-title",[e._v("Reiniciar Contraseña...")]),t("v-spacer")],1),t("v-card-text",[t("v-form",[t("v-text-field",{attrs:{"prepend-icon":"mdi-email",label:"Email",type:"text",disabled:"",rules:[e=>!!e||"E-mail es requerido!",e=>/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(e)||"E-mail no es válido"]},model:{value:e.email,callback:function(t){e.email=t},expression:"email"}}),t("v-text-field",{attrs:{id:"password","prepend-icon":"mdi-lock",label:"Contraseña",type:e.show_pwd?"text":"password","append-icon":e.show_pwd?"mdi-eye":"mdi-eye-off",rules:[e=>!!e||"Contraseña es requerida!",e=>/^\w(?=.{4,})/.test(e)||"Contraseña debe ser mínimo de 5 caracteres!"]},on:{"click:append":function(t){e.show_pwd=!e.show_pwd}},model:{value:e.password,callback:function(t){e.password=t},expression:"password"}}),t("v-text-field",{attrs:{id:"confirmation_password","prepend-icon":"lock",label:"Confirmación de Contraseña",type:e.show_conf_pwd?"text":"password","append-icon":e.show_conf_pwd?"mdi-eye":"mdi-eye-off",rules:[e=>!!e||"Contraseña es requerida!",e=>/^\w(?=.{4,})/.test(e)||"Contraseña debe ser mínimo de 5 caracteres!",e=>e===this.password||"La contraseña de confirmación no coincide!!"]},on:{"click:append":function(t){e.show_conf_pwd=!e.show_conf_pwd}},model:{value:e.password_confirmation,callback:function(t){e.password_confirmation=t},expression:"password_confirmation"}})],1)],1),t("v-card-actions",[t("v-spacer"),t("v-btn",{attrs:{color:"primary"},on:{click:e.cancel}},[e._v("Cancelar")]),t("v-btn",{attrs:{color:"primary",type:"submit"},on:{click:e.resetPassword}},[e._v("Cambiar contraseña")])],1)],1)],1)],1)],1)],1)],1)],1)},_e=[],he={data(){return{token:null,email:this.$route.params.email,password:null,password_confirmation:null,has_error:!1,show_pwd:!1,show_conf_pwd:!1}},methods:{cancel(){this.$router.replace("/")},resetPassword(){this.$axios.post("api/reset-password",{token:this.$route.params.token,email:this.$route.params.email,password:this.password,password_confirmation:this.password_confirmation}).then((e=>{console.log(e),this.$store.dispatch("login",{email:this.$route.params.email,password:this.password})})).catch((e=>{console.log(e.response),this.setFlashMessage({message:e.response.data.message,type:"error"})}))}}},pe=he,fe=(0,b.Z)(pe,me,_e,!1,null,null,null),ve=fe.exports;a["default"].use(n.og);const ge=(0,n.WB)();var we=ge;const ke=(e,t,s)=>{const a=v(we);a.isLoggedIn?s("/login"):s()},ye=(e,t,s)=>{const a=v(we);a.isLoggedIn?s():"/login"!==be.path&&s("/login")};a["default"].use(Z.ZP);const be=new Z.ZP({mode:"history",routes:[{path:"/",redirect:"/login"},{path:"/login",name:"Login",component:re,beforeEnter:ke},{path:"/forgot-password",name:"forgot-password",component:ue,meta:{auth:!1}},{path:"/reset-password/:email/:token",name:"reset-password-form",component:ve,meta:{auth:!1}},{path:"/home",name:"Home",component:G,beforeEnter:ye},{path:"/about",name:"About",component:()=>s.e(879).then(s.bind(s,9879))}]});var xe=be,$e=s(707),Ce=s.n($e),qe=(s(8556),s(2344)),Se=s(9694);a["default"].use(Se.Z),a["default"].use(qe.Z),a["default"].use(Ce()),we.use((({store:e})=>{e.router=(0,a.markRaw)(xe)})),a["default"].config.productionTip=!1,a["default"].prototype.$axios=l(),window.axios=s(6265),window.axios.defaults.headers.common["X-Requested-With"]="XMLHttpRequest",window.axios.interceptors.request.use((e=>{const t=localStorage.getItem("access_token");return t&&(e.headers["x-access-token"]=t),e}),(e=>{Promise.reject(e)})),new a["default"]({vuetify:new(Ce())({theme:{dark:!1},lang:{t:(e,...t)=>p.t(e,t)}}),pinia:we,i18n:p,router:xe,render:e=>e(U)}).$mount("#app")},8092:function(e,t,s){var a={"./en.json":790,"./es.json":8563};function o(e){var t=r(e);return s(t)}function r(e){if(!s.o(a,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return a[e]}o.keys=function(){return Object.keys(a)},o.resolve=r,e.exports=o,o.id=8092},790:function(e){"use strict";e.exports=JSON.parse('{"menus":{"active_source":"Active source","culture":"Culture","about":"About","delete_record_text":"Are you sure you want to delete this record?","delete_record_title":"Delete record","cancel":"Cancel","loading":"Loading..."},"main_page":{"period":"Period","area":"Area","questionaire_type":"Type of questionaire","question_theme":"Questions Theme","user":"User","question":"Question","answer":"Answer","actor_table":{"name":"Name","area":"Area","actions":"Actions"},"answer_saved":"Your answer has been saved!"},"login":{"email_required":"E-mail is required!","pwd_required":"Password is required!","password":"Password","forgot_pwd":"Forgot password?","min_pwd":"Password must be min 5 characters long!","email_not_valid":"Email is not valid!","pwd_not_valid":"Password is not valid!","missing_token":"Missing Token!","invalid_token":"Invalid Token!","missing_credentials":"Missing credentials!","user_not_registered":"User is not registered!","bad_credentials":"Invalid credentials!"}}')},8563:function(e){"use strict";e.exports=JSON.parse('{"menus":{"active_source":"Fuente Activa","culture":"Cultura","about":"Acerca de..","delete_record_text":"Está seguro de eliminar este registro?","delete_record_title":"Borrar registro","cancel":"Cancelar","loading":"Cargando..."},"main_page":{"period":"Periodo","area":"Area","questionaire_type":"Tipo de Cuestionario","question_theme":"Temáticas de las preguntas","user":"Empleado","question":"Pregunta","answer":"Respuesta","actor_table":{"name":"Nombre","area":"Area","actions":"Acciones"},"answer_saved":"Su respuesta ha sido guardada!"},"login":{"email_required":"E-mail es requerido!","pwd_required":"Contraseña es requerida!","password":"Contraseña","forgot_pwd":"¿Olvidó su contraseña?","min_pwd":"Contraseña debe ser mínimo de 5 caracteres!","email_not_valid":"E-mail no es válido!","pwd_not_valid":"Contraseña no es válida!","missing_token":"Token no está presente!","invalid_token":"Token inválido!","missing_credentials":"Faltan las credenciales!","user_not_registered":"Usuario no está registrado!","bad_credentials":"Credenciales incorrectas!"}}')}},t={};function s(a){var o=t[a];if(void 0!==o)return o.exports;var r=t[a]={exports:{}};return e[a].call(r.exports,r,r.exports,s),r.exports}s.m=e,function(){var e=[];s.O=function(t,a,o,r){if(!a){var n=1/0;for(d=0;d<e.length;d++){a=e[d][0],o=e[d][1],r=e[d][2];for(var i=!0,l=0;l<a.length;l++)(!1&r||n>=r)&&Object.keys(s.O).every((function(e){return s.O[e](a[l])}))?a.splice(l--,1):(i=!1,r<n&&(n=r));if(i){e.splice(d--,1);var c=o();void 0!==c&&(t=c)}}return t}r=r||0;for(var d=e.length;d>0&&e[d-1][2]>r;d--)e[d]=e[d-1];e[d]=[a,o,r]}}(),function(){s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,{a:t}),t}}(),function(){s.d=function(e,t){for(var a in t)s.o(t,a)&&!s.o(e,a)&&Object.defineProperty(e,a,{enumerable:!0,get:t[a]})}}(),function(){s.f={},s.e=function(e){return Promise.all(Object.keys(s.f).reduce((function(t,a){return s.f[a](e,t),t}),[]))}}(),function(){s.u=function(e){return"js/"+e+".4d9760ec.js"}}(),function(){s.miniCssF=function(e){return"css/"+e+".73f1fab9.css"}}(),function(){s.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="OA-HUB:";s.l=function(a,o,r,n){if(e[a])e[a].push(o);else{var i,l;if(void 0!==r)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var u=c[d];if(u.getAttribute("src")==a||u.getAttribute("data-webpack")==t+r){i=u;break}}i||(l=!0,i=document.createElement("script"),i.charset="utf-8",i.timeout=120,s.nc&&i.setAttribute("nonce",s.nc),i.setAttribute("data-webpack",t+r),i.src=a),e[a]=[o];var m=function(t,s){i.onerror=i.onload=null,clearTimeout(_);var o=e[a];if(delete e[a],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((function(e){return e(s)})),t)return t(s)},_=setTimeout(m.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=m.bind(null,i.onerror),i.onload=m.bind(null,i.onload),l&&document.head.appendChild(i)}}}(),function(){s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){s.p="/"}(),function(){var e=function(e,t,s,a){var o=document.createElement("link");o.rel="stylesheet",o.type="text/css";var r=function(r){if(o.onerror=o.onload=null,"load"===r.type)s();else{var n=r&&("load"===r.type?"missing":r.type),i=r&&r.target&&r.target.href||t,l=new Error("Loading CSS chunk "+e+" failed.\n("+i+")");l.code="CSS_CHUNK_LOAD_FAILED",l.type=n,l.request=i,o.parentNode.removeChild(o),a(l)}};return o.onerror=o.onload=r,o.href=t,document.head.appendChild(o),o},t=function(e,t){for(var s=document.getElementsByTagName("link"),a=0;a<s.length;a++){var o=s[a],r=o.getAttribute("data-href")||o.getAttribute("href");if("stylesheet"===o.rel&&(r===e||r===t))return o}var n=document.getElementsByTagName("style");for(a=0;a<n.length;a++){o=n[a],r=o.getAttribute("data-href");if(r===e||r===t)return o}},a=function(a){return new Promise((function(o,r){var n=s.miniCssF(a),i=s.p+n;if(t(n,i))return o();e(a,i,o,r)}))},o={143:0};s.f.miniCss=function(e,t){var s={879:1};o[e]?t.push(o[e]):0!==o[e]&&s[e]&&t.push(o[e]=a(e).then((function(){o[e]=0}),(function(t){throw delete o[e],t})))}}(),function(){var e={143:0};s.f.j=function(t,a){var o=s.o(e,t)?e[t]:void 0;if(0!==o)if(o)a.push(o[2]);else{var r=new Promise((function(s,a){o=e[t]=[s,a]}));a.push(o[2]=r);var n=s.p+s.u(t),i=new Error,l=function(a){if(s.o(e,t)&&(o=e[t],0!==o&&(e[t]=void 0),o)){var r=a&&("load"===a.type?"missing":a.type),n=a&&a.target&&a.target.src;i.message="Loading chunk "+t+" failed.\n("+r+": "+n+")",i.name="ChunkLoadError",i.type=r,i.request=n,o[1](i)}};s.l(n,l,"chunk-"+t,t)}},s.O.j=function(t){return 0===e[t]};var t=function(t,a){var o,r,n=a[0],i=a[1],l=a[2],c=0;if(n.some((function(t){return 0!==e[t]}))){for(o in i)s.o(i,o)&&(s.m[o]=i[o]);if(l)var d=l(s)}for(t&&t(a);c<n.length;c++)r=n[c],s.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return s.O(d)},a=self["webpackChunkOA_HUB"]=self["webpackChunkOA_HUB"]||[];a.forEach(t.bind(null,0)),a.push=t.bind(null,a.push.bind(a))}();var a=s.O(void 0,[998],(function(){return s(7411)}));a=s.O(a)})();
//# sourceMappingURL=app.ab713f19.js.map