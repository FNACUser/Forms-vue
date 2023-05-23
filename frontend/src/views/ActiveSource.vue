<template>
  <v-container class="px-10" fluid>
    <br />
    <v-row>
      <v-col class="d-flex justify-space-around mb-6 align-end" cols="2">
        <v-select 
            v-model="mainStore.selected_cycle" 
            :items="mainStore.filteredCycles" 
            :label="$t('globals.period')"
            :item-text="`Cycle_${$i18n.locale}`" 
            item-value="id_cycle" 
            clearable 
            dense>
        </v-select>
      </v-col>
      <v-col cols="2" class="d-flex justify-space-around mb-6 align-end" v-if="mainStore.selected_cycle">
        <v-select 
            v-model="selected_network" 
            :items="mainStore.networks" 
            :label="$t('active_source.questionaire_type')"
            :item-text="`name_${$i18n.locale}`" 
            item-value="id" 
            clearable 
            return-object 
            @click:clear="clearVariables"
            @change="getData()" 
            dense>
        </v-select>
      </v-col>

      <v-col cols="3" class="d-flex justify-space-around mb-6 align-end" v-if="filteredNetwokModeThemes">
        <v-select 
            v-model="selected_network_mode_theme" 
            :items="filteredNetwokModeThemes"
            :label="$t('active_source.question_theme')" 
            :item-text="`Network_mode_theme_${$i18n.locale}`"
            item-value="id_network_mode_theme" 
            clearable @change="getData()" 
            @click:clear="clearVariables" 
            dense>
        </v-select>
      </v-col>

      <v-col class="d-flex justify-space-around mb-6 align-end" cols="6"
        v-if="selected_network && selected_network.code === 'explora'">
        <v-autocomplete 
            v-model="selected_tools" 
            :items="user_tools" 
            :item-text="`name_${$i18n.locale}`" 
            item-value="id"
            :label="$t('active_source.tools')" 
            multiple  
            return-object
            dense 
            :disabled="currentForm && currentForm.is_concluded" 
            @change="removeToolsIfDeselected()"
        >
              <template v-slot:selection="{ attrs, item, selected }">
                <v-chip
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    small
                    @click:close="delRecord(item.id, 'menus.delete_record_title', 'alerts.delete_tool_text', selected_network[`name_${$i18n.locale}`], 'Explora')"
                >
                   {{ item[`name_${$i18n.locale}`] }}
                </v-chip>
              </template>
          </v-autocomplete>
      </v-col>

      <v-col cols="2" class="d-flex justify-space-around mb-6 align-end"
          v-if="selected_network && selected_network.code === 'actor'">
          <v-autocomplete 
              v-model="selected_area" 
              :items="mainStore.areas" 
              :label="$t('active_source.area')"
              :item-text="`Organization_area_${$i18n.locale}`" 
              item-value="id_organization_area" 
              clearable 
              dense
              :disabled="currentForm && currentForm.is_concluded">
          </v-autocomplete>
      </v-col>

      <v-col class="d-flex justify-space-around mb-6 align-end" cols="3"
          v-if="selected_network && selected_network.code === 'actor'">
          <v-autocomplete 
              v-model="selected_actors" 
              :items="filteredEmployees" 
              item-text="username" 
              item-value="id"
              :label="$t('active_source.user')" 
              persistent-hint 
              small-chips 
              multiple 
              return-object
              @change="addInteractingActor()" 
              dense 
              :disabled="currentForm && currentForm.is_concluded"
              >
          </v-autocomplete>
      </v-col>

    </v-row>
    <v-row v-if="mainStore.network_modes.length">
      <v-col cols="2" v-for="(form, index) in forms" :key="index">
        <gauge :label="form[`name_${$i18n.locale}`]"
          :in_value="Math.round(form['answers'] * 100 / (form['total_questions'] * form['total_items']))"
          :in_size="((current_network_mode && form.id == current_network_mode.id_network_mode) ? 100 : 60)"
          :in_width="((current_network_mode && form.id == current_network_mode.id_network_mode) ? 15 : 7)"
          @click.native="setSelectedNetworkAndTheme(form)" />

      </v-col>
    </v-row>
    <v-row v-if="current_network_mode">
      <v-col cols="3">

        <v-switch v-model="currentForm.is_concluded"
          :label="`${$t('active_source.section_closed')}: ${getFormSectionName(this.current_network_mode, this.$i18n.locale)}`"
          @change="toggleOpenCloseCurrentForm" v-if="currentForm"></v-switch>

      </v-col>

      <v-col 
        v-if="selected_network && ['educ_model', 'resource'].includes(selected_network.code) && currentForm && !currentForm.is_concluded"
        class="d-flex justify-end mr-11">
        <add-node 
          :label="selected_network[`name_${$i18n.locale}`]"
          :network_mode_id="current_network_mode.id_network_mode" 
          @newnode="refreshNodes">
        </add-node>
      </v-col>


      <v-col  
          v-if="selected_network && selected_network.code=== 'narrative' && currentForm && !currentForm.is_concluded"
          class="d-flex justify-end mr-11">
          <add-narrative
              :showNarrativeDialog.sync="showNarrativeDialog"
              :label="selected_network[`name_${$i18n.locale}`]"
              :network_mode_id="current_network_mode.id_network_mode" 
              :mode="narrativeDialogMode"
              :item="narrativeItem"
              @new_narrative="addNarrative"
              @narrative_updated="updateNarrative"
              @close="closeNarrativeDialog"
            >
          </add-narrative>
      </v-col>


    </v-row>

    <v-row dense justify="space-around">
      <v-col cols="3" v-if="selected_network && !['explora','narrative'].includes(selected_network.code)">
        <div v-for="(item, i) in questions" :key="i">
          <v-card>
            <v-app-bar flat color="blue">
              <v-card-title class="white--text">
                {{ $t('active_source.question') }} {{ i + 1 }}
              </v-card-title>
            </v-app-bar>
            <v-card-text>{{ item[`Question_${$i18n.locale}`] }}</v-card-text>
          </v-card>
          <br />
        </div>
      </v-col>

      <v-col cols="8" v-if="selected_network && selected_network.code === 'actor'">

        <v-data-table 
            :headers="tableActorsHeader" 
            :items="selected_actors" 
            :items-per-page="-1" 
            class="elevation-1"
            v-if="selected_actors.length > 0" 
            dense>
          <template v-slot:item="{ item }">

            <tr>
              <td class="text-xs-left">{{ item.username }}</td>
              <td class="text-xs-left">{{ item.organization_area[`Organization_area_${$i18n.locale}`] }}</td>
              <template>
                <td v-for="(question, index) in questions" :key="index" class="">

                  <v-select 
                      :id="`sel_${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`"
                      v-model="answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`]"
                      :items="JSON.parse(question.question_possible_answers[`Question_possible_answers_${$i18n.locale}`])"
                      item-text="texto" 
                      item-value="valor" 
                      clearable
                      @change="saveAnswersArray($event, item.id, question.id_question)"
                      :multiple="question.question_possible_answers.multiple" deletable-chips small-chips outlined flat
                      rounded 
                      class="my-5" dense :disabled="currentForm && currentForm.is_concluded"
                  >
                  </v-select>

                </td>
              </template>
              <td>

                <v-tooltip bottom v-if="!selected_network_mode_theme || (currentForm && !currentForm.is_concluded)">
                  <template #activator="{ on }">
                    <v-icon v-on="on" small
                      @click="delRecord(item.id, 'menus.delete_record_title', 'alerts.delete_interacting_person_text', selected_network[`name_${$i18n.locale}`], 'Actor')"
                      color="orange">
                      mdi-delete
                    </v-icon>
                  </template>
                  <span>{{ $t('menus.delete') }}</span>
                </v-tooltip>

              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>

      <v-col cols="8" v-if="selected_network && ['educ_model', 'resource'].includes(selected_network.code)">

        <v-data-table 
            :headers="tableNodesHeader" 
            :items="filteredNodes" 
            :items-per-page="-1" 
            class="elevation-1"
            v-if="nodes" 
            dense>
          <template v-slot:item="{ item }">

            <tr>
              <td class="text-xs-left">
                {{ item[`Node_${$i18n.locale}`] }}
              </td>

              <template>
                <td v-for="(question, index) in questions" :key="index">

                  <v-select 
                    :id="`sel_${current_network_mode.id_network_mode}_${question.id_question}_${item.id_node}`"
                    v-model="answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id_node}`]"
                    :items="JSON.parse(question.question_possible_answers[`Question_possible_answers_${$i18n.locale}`])"
                    item-text="texto" 
                    item-value="valor" 
                    clearable
                    @change="saveAnswersArray($event, item.id_node, question.id_question)"
                    :multiple="question.question_possible_answers.multiple" 
                    deletable-chips 
                    small-chips 
                    outlined 
                    flat
                    rounded 
                    class="my-5" 
                    dense 
                    :disabled="currentForm && currentForm.is_concluded"
                  >
                  </v-select>

                </td>
              </template>
              <td>

                <v-tooltip bottom
                  v-if="(mainStore.logged_user.id == item.id_employee) && currentForm && !currentForm.is_concluded">
                  <template #activator="{ on }">
                    <v-icon v-on="on" small
                      @click="delRecord(item.id_node, 'menus.delete_record_title', 'alerts.delete_item_text', selected_network[`name_${$i18n.locale}`], 'Node')"
                      color="orange">
                      mdi-delete
                    </v-icon>
                  </template>
                  <span>{{ $t('menus.delete') }}</span>
                </v-tooltip>

              </td>

            </tr>
          </template>
        </v-data-table>
      </v-col>

      <v-col cols="12" v-if="selected_network && selected_network.code === 'explora'">

        <v-data-table 
          :headers="tableToolsHeader" 
          :items="selected_tools" 
          :items-per-page="-1" 
          class="elevation-1"
          v-if="selected_tools.length > 0" 
          fixed-header
          hide-default-footer
          disable-pagination
          height="500"
          dense
          
        >
          <template v-slot:item="{ item }">
            <tr>
              <td class="text-xs-left" style="width:15%">{{ item[`name_${$i18n.locale}`] }}</td>
              <template>
                <td v-for="(question, index) in filteredQuestions" :key="index" style="width:7%">

                  <v-select 
                    :id="`sel_${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`"
                    v-model="answers[`${current_network_mode.id_network_mode}_${question.id_question}_${item.id}`]"
                    :items="JSON.parse(question.question_possible_answers[`Question_possible_answers_${$i18n.locale}`])"
                    item-text="texto" 
                    item-value="valor" 
                    clearable
                    @change="saveAnswersArray($event, item.id, question.id_question)"
                    :multiple="question.question_possible_answers.multiple" 
                    deletable-chips 
                    small-chips 
                    outlined 
                    flat
                    rounded 
                    class="my-5" 
                    dense 
                    :disabled="currentForm && currentForm.is_concluded"
                  >
                  </v-select>

                </td>
              </template>
              <td>
                <div v-if="item.options && item.options.length > 0 && externalSourceQuestion && answers[`${current_network_mode.id_network_mode}_${externalSourceQuestion.id_question}_${item.id}`]">
                  <ul>
                      <li
                        v-for="(optionID, index) in answers[`${current_network_mode.id_network_mode}_${externalSourceQuestion.id_question}_${item.id}`]" :key="index"
                      >
                        {{ item.options.find(obj =>  obj.id === optionID)[`name_${$i18n.locale}`]}}
                        <v-icon
                            small
                            color="red darken-2"
                            @click="deleteSelectedOption(current_network_mode.id_network_mode,externalSourceQuestion.id_question,item.id,index)"
                            v-if="currentForm && !currentForm.is_concluded"
                          >
                            mdi-close-circle-outline
                        </v-icon>
                      </li>
                  </ul>
                </div>
              </td>

              <td align="right">

                <v-tooltip bottom v-if="currentForm && !currentForm.is_concluded">
                  <template #activator="{ on }">
                    <v-icon v-on="on" small @click="showUsageOptionsDialog(item,externalSourceQuestion.id_question)" color="green">
                      mdi-form-select
                    </v-icon>
                  </template>
                  <span>{{ $t('menus.select_usage_options') }} </span>
                </v-tooltip>

                <v-tooltip bottom v-if="currentForm && !currentForm.is_concluded">
                  <template #activator="{ on }">
                    <v-icon v-on="on" small
                      @click="delRecord(item.id, 'menus.delete_record_title', 'alerts.delete_tool_text', selected_network[`name_${$i18n.locale}`], 'Explora')"
                      color="orange">
                      mdi-delete
                    </v-icon>
                  </template>
                  <span>{{ $t('menus.delete') }}</span>
                </v-tooltip>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>


      <v-col cols="12" v-if="selected_network && selected_network.code === 'narrative'">

          <v-data-table 
            :headers="defaultNarrativesHeader" 
            :items="narratives" 
            :items-per-page="-1" 
            class="elevation-1"
            v-if="narratives.length > 0"   
            hide-default-footer
            disable-pagination
            dense
          >
            <template v-slot:item="{ item }">
              <tr>
                <td class="text-xs-left" style="width:25%">
                    {{ item['title'] }}
                </td>
                <td style="width:50%">
                    {{ item['narrative'] }}
                </td>
                <td align="right">

                  <v-tooltip bottom v-if="currentForm && !currentForm.is_concluded">
                    <template #activator="{ on }">
                      <v-icon v-on="on" 
                        small  
                        color="green"
                        @click="editNarrative(item)"
                        
                        >
                        mdi-pencil
                      </v-icon>
                    </template>
                    <span>{{ $t('globals.edit') }} </span>
                  </v-tooltip>

                  <v-tooltip bottom v-if="currentForm && !currentForm.is_concluded">
                    <template #activator="{ on }">
                      <v-icon v-on="on" small
                        @click="delRecord(item.id, 'menus.delete_record_title', 'alerts.delete_narrative_text', selected_network[`name_${$i18n.locale}`], 'Narrative')"
                        color="orange">
                        mdi-delete
                      </v-icon>
                    </template>
                    <span>{{ $t('globals.delete') }}</span>
                  </v-tooltip>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-col>


    </v-row>

    <confirmation-dialog ref="confirmDeleteActor" />

    <UsageOptionsDialog 
      :usageOptions="toolOptions"
      :toolID="toolID"
      :questionID="questionID"
      :defaultOptions="selected_options"
      :showDialog="openUsageOptionsDialog"
      @close="closeUsageOptionsDialog" 
      @usageOptionsSelected="saveAnswersArray($event.selected_options, $event.toolID, $event.questionID)"

    ></UsageOptionsDialog>

  </v-container>
</template>
<script>

import { useMainStore } from '@/store/main';
import { mapStores, mapState } from 'pinia';
import ConfirmationDialog from '@/components/partials/ConfirmationDialog.vue';
import Gauge from '@/components/Gauge.vue';
import AddNode from '@/components/AddNode.vue';
import AddNarrative from '@/components/AddNarrative.vue';
import UsageOptionsDialog from '@/components/UsageOptionsDialog.vue';


export default {

  components: {
    ConfirmationDialog,
    Gauge,
    AddNode,
    AddNarrative,
    UsageOptionsDialog
  },

  data() {
    return {

      selected_actors: [],
      selected_tools: [],
      narratives:[],
      user_tools: [],
      selected_options:[],
      selected_network: null,
      selected_area: null,
      selected_node_segment_category: null,
      selected_network_mode_theme: null,
      questions: [],
      answers: {},
      nodes: [],
      current_network_mode: null,
      formClosed: false,
      adjacency_input_forms: [],
      forms: [],
      openUsageOptionsDialog: false,
      toolOptions: [],
      toolID:null,
      questionID: null,
      showNarrativeDialog: false,
      narrativeDialogMode: 'create',
      narrativeItem:null,
      
      selRules: [

        v => (v && v.length <= 2) || 'Máximo 2 opciones!! ${v.length}',
      ],

      defaultActorsHeader: [
        {
          text: 'Nombre',
          align: 'start',
          value: 'username',
          class: "white--text"
        },
        {
          text: 'Area',
          value: 'id_organization_area',
          class: "white--text"
        },

        {
          text: 'Acciones',
          class: "white--text",
          sortable: false
        },
      ],


      defaultNodesHeader: [
        {
          text: 'Nombre',
          align: 'start',
          value: 'name',
          class: "white--text"
        },
        {
          text: 'Acciones',
          class: "white--text",
          sortable: false
        },
      ],

      defaultToolsHeader: [
        {
          text: 'Herramienta',
          align: 'start',
          value: 'username',
          class: "white--text"
        },
        {
          text: 'Acciones',
          class: "white--text",
          align: 'end',
          sortable: false
        },
      ],

      defaultNarrativesHeader: [
        {
          text: 'Título',
          align: 'start',
          value: 'title',
          class: "white--text"
        },
        {
          text: 'Narrativa',
          align: 'start',
          value: 'narrative',
          class: "white--text"
        },
        {
          text: 'Acciones',
          class: "white--text",
          align: 'end',
          sortable: false
        },
      ]

    }
  },


  

  mounted() {

    this.initialize();
  },

  watch: {

    selected_cycle(new_val) {

      if (new_val == null) {

        this.resetSelectedVariables();
      }
      else {

        this.initialize();

      }
    }


  },


  computed: {

    ...mapState(useMainStore, ["selected_cycle"]),
    ...mapStores(useMainStore),


    current_adjacency_input_form_id() {

      let form_id = null;
      if (this.current_network_mode && this.mainStore.selected_cycle && this.mainStore.logged_user) {

        form_id = `${this.mainStore.selected_cycle}-${this.mainStore.logged_user.id}-${this.current_network_mode.id_network_mode}`;

      }

      return form_id;

    },


    currentForm() {

      if (this.forms.length) {

        //console.log("dentro de computed currentForm");

        if (this.current_adjacency_input_form_id) {

          const adj_form = this.forms.filter(item => item.id_adjacency_input_form == this.current_adjacency_input_form_id);

          //  console.log(adj_form);

          if (adj_form.length) {

            return adj_form[0];

          }

        }
      }

      return null;


    },


    interactingPeopleIds() {


      if (this.selected_actors) {

        return this.selected_actors.map(a => a.id);

      }

      return [];
    },


    // filteredCycles(){
    //   return this.mainStore.cycles.filter(item=> item.Is_active); 
    // },

    filteredNodes() {
      return this.nodes.filter(item => (item.id_employee == this.mainStore.logged_user.id) || (item.id_employee == null));
    },

    filteredEmployees() {


      if (this.selected_area) {

        return this.mainStore.employees.filter(item => item.id_organization_area === this.selected_area);

      }
      else return null;

    },



    //filters all questions that do not use any  external source 
   
    filteredQuestions() {


      if (this.selected_network && this.selected_network.code == 'explora' && this.questions.length > 0) {

        return this.questions.filter(item => !item.question_possible_answers.use_external_source);

      }
      else return [];

    },


    externalSourceQuestion(){

      if (this.selected_network && this.selected_network.code == 'explora' && this.questions.length > 0) {

        const question_external_source= this.questions.find(item => item.question_possible_answers.use_external_source);
        
        return question_external_source;

      }
        else return null;

    },




    filteredNetwokModeThemes() {

      if (this.selected_network) {

        let filteredArr = this.mainStore.network_modes.filter(item => item.id_network === this.selected_network.id && item.network_mode_theme);

        if (filteredArr && filteredArr.length) {
          return filteredArr.map(item => {
            return item.network_mode_theme;

          });
        }
        else return null;
      }
      else
        return null;

    },

    tableActorsHeader() {

      return this.makeActorsTableHeader(this.questions, this.defaultActorsHeader, this.$t('active_source.question'));

    },

    tableNodesHeader() {

      return this.makeNodesTableHeader(this.questions, this.defaultNodesHeader, this.$t('active_source.question'));

    },


    tableToolsHeader() {

      return this.makeToolsTableHeader(this.questions, this.defaultToolsHeader);

    },


  },


  methods: {


   async  removeToolsIfDeselected(){

      const saved_tools_ids = this.getSavedToolsIds();

      const selected_tools_ids = this.selected_tools.map(item => item.id);
    
      // if(saved_tools_ids.length>=selected_tools_ids.length){

        const deselected_tool_id = saved_tools_ids.filter(f => !selected_tools_ids.includes(f))[0];
        
        if(deselected_tool_id){
          
          if (await this.$refs.confirmDeleteActor.open(this.$t('menus.delete_record_title'), this.$t('alerts.delete_tool_text', { item: this.selected_network[`name_${this.$i18n.locale}`] }), { color: "red lighten-3" })) {

            await  this.deleteSelectedTool(deselected_tool_id, false);
          }
          else {

            this.selected_tools.push(this.user_tools.filter(item=> item.id==deselected_tool_id)[0]);

          }
      // }
       

      }

    },


    deleteSelectedOption(networkModeID, questionID, toolID, index){

        this.answers[`${networkModeID}_${questionID}_${toolID}`].splice(index,1);
        this.saveAnswersArray(this.answers[`${networkModeID}_${questionID}_${toolID}`], toolID, questionID);

    },


    getSavedSelectedTools(){

      //  console.log('Entra a getAnswerKeys');
      const tools_ids= this.getSavedToolsIds();
      if( tools_ids.length>0){

        let  selected_tools=[];
        tools_ids.forEach(id =>  selected_tools.push(this.user_tools.filter(item=> item.id==id)[0]));

        return selected_tools;
      }
      return [];

    },

    getSavedToolsIds(){

      
      if( Object.keys(this.answers).length>0){

        const network_mode=this.mainStore.network_modes.filter(item => item.network.code === 'explora')[0];

        return  [...new Set(Object.keys(this.answers).filter(item => item.split('_')[0]==network_mode.id_network_mode).map(item => parseInt(item.split('_')[2])))];

      }
      return [];

      },



    showUsageOptionsDialog(item, question_id) {


      if (item && item.options.length > 0){
        this.toolOptions = item.options;
        this.toolID=item.id;
        this.questionID = question_id;
        if (this.current_network_mode) {
          this.selected_options = this.answers[`${this.current_network_mode.id_network_mode}_${question_id}_${item.id}`] ?? []; 
        }
        
      }
        
      this.openUsageOptionsDialog = true;

      // console.log(this.openUsageOptionsDialog);

    },

   
    closeUsageOptionsDialog(){

      this.openUsageOptionsDialog = false;
      this.toolOptions = [];
      this.selected_options = [];

    },

    closeNarrativeDialog() {

      // console.log(' entro a closeNarrativeDialog');
      this.showNarrativeDialog = false;
      this.narrativeDialogMode = 'create';
      this.narrativeItem = null;
      
    },


    refreshNodes(new_nodes) {

      this.nodes = new_nodes;
      this.updateNetworkModeGauge(this.current_network_mode)

    },

    addNarrative(new_narrative) {

      this.narratives.push(new_narrative);
      this.updateNetworkModeGauge(this.current_network_mode)

    },

    updateNarrative(inputObj) {

      const index = this.narratives.findIndex(item => item.id == inputObj.narrative_id);

      this.narratives[index]['title'] = inputObj.title;
      this.narratives[index]['narrative'] = inputObj.narrative;
      
    },


    setSelectedNetworkAndTheme(form) {


      this.selected_network = form.network_mode.network;

      if (this.selected_network.code == 'actor') {

        this.selected_network_mode_theme = form.network_mode.network_mode_theme.id_network_mode_theme;

      }
      else {

        this.selected_network_mode_theme = null;

      }

      
      this.getData();

    },


    getFormSectionName(netw_mode, lang) {

      return netw_mode && netw_mode.network ? (netw_mode.network_mode_theme ? netw_mode.network[`name_${lang}`] + '-' + netw_mode.network_mode_theme[`Network_mode_theme_${lang}`] : netw_mode.network[`name_${lang}`]) : '';

    },



    saveAnswersArray(event, item_id, question_id) {

    
      // console.log(event);
      if (this.answers[`${this.current_network_mode.id_network_mode}_${question_id}_${item_id}`]) {

        this.answers[`${this.current_network_mode.id_network_mode}_${question_id}_${item_id}`] = event;

      }
      else {

        this.$set(this.answers, `${this.current_network_mode.id_network_mode}_${question_id}_${item_id}`, event);

      }


      const data = {
        "cycle_id": this.mainStore.selected_cycle,
        "user_email": this.mainStore.logged_user.email,
        "item_id": item_id,
        "question_id": question_id,
        "network_mode_id": this.current_network_mode.id_network_mode,
        // "network_mode_theme_id":this.selected_network_mode_theme,
        "selected_option": event
      };

      this.$axios.post(process.env.VUE_APP_BACKEND_URL + '/save_answer', data)
        .then(async response => {
          //console.log(response.data.responses);

          //this.$alertify.success(this.$t(response.data.message));

          this.populateAnswers(response.data.responses);
          this.updateNetworkModeGauge(this.current_network_mode);


        })
        .catch(error => {
          this.$alertify.error(this.$t(error.message));
          console.error('There was an error!', error.message);
          console.error(error);
        });

    },


    updateNetworkModeGauge(network_mode) {

      const index = this.forms.findIndex(item => item.id == network_mode.id_network_mode);


      if(['actor','resource', 'educ_model','explora'].includes(network_mode.network.code )){
        const prefix = network_mode.id_network_mode + '_';
        const num_answers = Object.keys(this.answers).filter(item => item.startsWith(prefix)).length;
        this.forms[index]['answers'] = num_answers;

      }
      else if (network_mode.network.code == 'narrative') {
        // console.log(this.narratives.length);
        this.forms[index]['answers'] = this.narratives.length;

      }

      if (network_mode.network.code == 'actor') {
        this.forms[index]['total_items'] = this.selected_actors.length > 0 ? this.selected_actors.length : 1;

      }
      else if (['resource', 'educ_model'].includes(network_mode.network.code)) {

        this.forms[index]['total_items'] = this.filteredNodes.length > 0 ? this.filteredNodes.length : 1;

      }
      else if (network_mode.network.code == 'explora') {
        this.forms[index]['total_items'] = this.selected_tools.length > 0 ? this.selected_tools.length : 1;

      }
      else if (network_mode.network.code == 'narrative') {
        this.forms[index]['total_items'] = this.narratives.length > 0 ? this.narratives.length : 1;

      }


    },


    updateAllActorNetworkModeGauges() {

      this.mainStore.network_modes.forEach(network_mode => {

        if (network_mode.network.code == 'actor') {
          this.updateNetworkModeGauge(network_mode);
        }

      })

    },



    makeActorsTableHeader(val, defaultHeader, text) {

      let headers = Object.assign([], defaultHeader);

      if (val && val.length > 0) {

        val.forEach((question, index) => {
          headers.splice(2 + index, 0, {
            text: `${text} ${index + 1}`,
            align: 'center',
            class: 'white--text',
            sortable: false,
          });
        });
      }

      headers[0].text = this.$t('active_source.actor_table.name');
      headers[1].text = this.$t('active_source.actor_table.area');
      headers[headers.length - 1].text = this.$t('active_source.actor_table.actions');

      return headers;

    },


    makeNodesTableHeader(val, defaultHeader, text) {

      let headers = Object.assign([], defaultHeader);

      if (val && val.length > 0) {

        val.forEach((question, index) => {
          headers.splice(1 + index, 0, {
            text: `${text} ${index + 1}`,
            align: 'center',
            class: 'white--text',
            sortable: false,
          });
        });
      }

      headers[0].text = this.selected_network[`name_${this.$i18n.locale}`];

      return headers;


    },


    makeToolsTableHeader(val, defaultHeader) {

      let headers = Object.assign([], defaultHeader);

      if (val && val.length > 0) {

        val.forEach((question, index) => {
          headers.splice(1 + index, 0, {
            text: question[`Question_${this.$i18n.locale}`],
            align: 'center',
            class: 'white--text',
            sortable: false,
          });
        });
      }

      headers[0].text = this.$t('active_source.tools');
      headers[headers.length - 1].text = this.$t('active_source.actor_table.actions');

      return headers;


    },

    sortSelectedColleagues() {
      this.selected_actors.sort((a, b) =>
        (a.username.toLowerCase() < b.username.toLowerCase()) ? -1 : ((b.username.toLowerCase() > a.username.toLowerCase()) ? 1 : 0));

    },


    async toggleOpenCloseCurrentForm() {

      // gets last selected person pushed into the list 
      const data = {
        "closed": this.currentForm.is_concluded,
        "id_adjacency_input_form": this.currentForm.id_adjacency_input_form,
        "user": JSON.stringify(this.mainStore.logged_user)
      };

      // console.log(data)
      await this.$axios.post(process.env.VUE_APP_BACKEND_URL + '/open_close_adjacency_input_form', data)
        .then(response => {
          this.$alertify.success(this.$t(response.data));
        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

      //this.sortSelectedColleagues();

    },



    async addInteractingActor() {


      // gets last selected person pushed into the list 
      const data = {
        "user_email": this.mainStore.logged_user.email,
        "employee_ids": this.interactingPeopleIds,
        "cycle_id": this.mainStore.selected_cycle
      };


      await this.$axios.post(process.env.VUE_APP_BACKEND_URL + '/add_interacting_actor', data)
        .then(response => {
          this.$alertify.success(this.$t(response.data));
          this.updateAllActorNetworkModeGauges();

        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

      this.sortSelectedColleagues();

    },

   


    async delRecord(itemID, title, message, item_name, type) {


      if (await this.$refs.confirmDeleteActor.open(this.$t(title), this.$t(message, { item: item_name }), { color: "red lighten-3" })) {

        if (type == 'Actor') {
          await this.deleteActor(itemID);
        }
        else if (type == 'Node') {

          await this.deleteNode(itemID);

        }
        else if (type == 'Explora') {

          await this.deleteSelectedTool(itemID, true);

        }

        else if (type == 'Narrative') {

          await this.deleteNarrative(itemID, true);

        }

      }
    },


    editNarrative(item) {
      // console.log(item);
      this.narrativeDialogMode = 'edit';
      this.narrativeItem = item;
      this.showNarrativeDialog = true;

    
    },

  
    async deleteNarrative(itemID, spliceArray) {

      let item_index = null;
      if (spliceArray) {
        item_index = this.narratives.findIndex(object => {
          return object.id == itemID
        });
      }

      const data = {
        "user_email": this.mainStore.logged_user.email,
        "item_id": itemID,
        "cycle_id": this.mainStore.selected_cycle,
        "network_mode_id": this.current_network_mode.id_network_mode
      };

      // console.log(data);

      await this.$axios.delete(process.env.VUE_APP_BACKEND_URL + '/user/narrative/delete', { data: data })
        .then(async response => {
          // console.log(response.data);
          this.$alertify.success(this.$t(response.data, { item: this.selected_network[`name_${this.$i18n.locale}`] }));
          if (spliceArray) this.narratives.splice(item_index, 1);
         
          this.updateNetworkModeGauge(this.current_network_mode);

        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });


    },

    async deleteSelectedTool(itemID,spliceArray) {

        let item_index =null;
        if(spliceArray){
          item_index = this.selected_tools.findIndex(object => {
              return object.id == itemID
            });
        }  

          const data = {
            "user_email": this.mainStore.logged_user.email,
            "item_id": itemID,
            "cycle_id": this.mainStore.selected_cycle,
            "network_mode_id": this.current_network_mode.id_network_mode
          };

          // console.log(data);

          await this.$axios.delete(process.env.VUE_APP_BACKEND_URL + '/selected_tool', { data: data })
            .then(async response => {
              // console.log(response.data);
              this.$alertify.success(this.$t(response.data.message, { item: this.selected_network[`name_${this.$i18n.locale}`] }));
              if(spliceArray) this.selected_tools.splice(item_index, 1);
              await this.getUserResponses();
              this.updateNetworkModeGauge(this.current_network_mode);

            })
            .catch(error => {

              console.error('There was an error!', error.message);
            });


    },

    async deleteNode(itemID) {

      const item_index = this.nodes.findIndex(object => {
        return object.id_node == itemID
      });

      const data = {
        "user_email": this.mainStore.logged_user.email,
        "item_id": itemID,
        "cycle_id": this.mainStore.selected_cycle,
        "network_mode_id": this.current_network_mode.id_network_mode
      };

      // console.log(data);

      await this.$axios.delete(process.env.VUE_APP_BACKEND_URL + '/node', { data: data })
        .then(async response => {
          // console.log(response.data);
          this.$alertify.success(this.$t(response.data.message, { item: this.selected_network[`name_${this.$i18n.locale}`] }));
          this.nodes.splice(item_index, 1);
          await this.getUserResponses();
          this.updateNetworkModeGauge(this.current_network_mode);

        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });


    },



    async deleteActor(itemID) {

      const item_index = this.selected_actors.findIndex(object => {
        return object.id == itemID
      });

      const data = {
        "user_email": this.mainStore.logged_user.email,
        "item_id": itemID,
        "cycle_id": this.mainStore.selected_cycle,
        "network_id": this.selected_network.id
      };

      await this.$axios.delete(process.env.VUE_APP_BACKEND_URL + '/delete_interacting_actor', { data: data })
        .then(async response => {
          // console.log(response.data);
          this.$alertify.success(this.$t(response.data));
          this.selected_actors.splice(item_index, 1);
          await this.getUserResponses();

          this.updateAllActorNetworkModeGauges();
          //this.createFormsDetails();
        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

    },


    resetSelectedVariables() {

      this.selected_area = null;
      this.mainStore.selected_cycle = null;
      this.selected_actors = null;
      this.selected_network = null;
      this.selected_node_segment_category = null;
      this.selected_network_mode_theme = null;
      this.questions = [];
      this.nodes = [];
      this.current_network_mode = null;
      this.answers = [];
      this.mainStore.network_modes = [];
      this.forms = [];
      this.selected_tools=[];
      this.selected_options=[];
      this.user_tools=[];

    },


    clearVariables() {

      this.questions = [];
      this.selected_network_mode_theme = null;
      this.current_network_mode = null;
      this.nodes = [];
      this.selected_tools=[];
      this.selected_options=[];
      this.user_tools=[];

    },

    async getNodes(network_mode_id) {

      if (network_mode_id) {

        const nodes = await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/network_mode/' + network_mode_id + '/nodes');
        this.nodes = nodes.data;
      }
      //return  nodes.data;
      // console.log(this.nodes);

    },


    async getActors() {

      await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/user/' + this.mainStore.logged_user.id + '/cycle/' + this.mainStore.selected_cycle + '/interacting_actors')
        .then(response => {
          const actor_ids = response.data;
          this.selected_actors = this.mainStore.employees.filter(item => actor_ids.includes(item.id));
        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

    },


    async getUserResponses() {

       await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/user/' + this.mainStore.logged_user.id + '/cycle/' + this.mainStore.selected_cycle + '/responses')
        .then(response =>  { 

          const responses = response.data;
          this.extractAjacencyInputForms(responses);
          this.populateAnswers(responses);
        
        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

    },


    async getUserAdjancencyInputForms() {

      await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/user/' + this.mainStore.logged_user.id + '/cycle/' + this.mainStore.selected_cycle + '/adjacency_input_forms')
        .then(response => {

          this.adjacency_input_forms = response.data;

        })
        .catch(error => {

          console.error('There was an error!', error.message);
        });

    },


    extractAjacencyInputForms(responses) {


      //console.log('entra a extractAjacencyInputForms');

      this.adjacency_input_forms = [];

      if (responses.length > 0) {
        //  console.log('pasa el if extractAjacencyInputForms')

        const arrayUniqueByKey = [...new Map(responses.map(item => [item.id_adjacency_input_form, item.adjacency_input_form])).values()];

        this.adjacency_input_forms = arrayUniqueByKey;


      }

    },


    populateAnswers(responses) {

      // console.log("entra a populateAnswers");

      if (responses.length) {
        this.answers = {};

        responses.forEach(response => {

          const resp_content = JSON.parse(response.Response);

          //console.log(resp_content);

          resp_content.forEach(content => {

            this.$set(this.answers, `${response.adjacency_input_form['id_network_mode']}_${response.id_question}_${content.item_id}`, content.valor);

          });

        });
      }
    },


    async getNetworkModeQuestions(selected_network_mode) {

      if (selected_network_mode) {
        const resp = await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/network_mode/' + selected_network_mode + '/questions');
        // console.log(resp);
        // this.questions=resp.data;
        return resp.data;
      }

    },


    getCurrentNetworkMode(){

      let current_network_mode = [];

      if (this.selected_network && this.filteredNetwokModeThemes) {

        if (this.selected_network_mode_theme) {

          current_network_mode = this.mainStore.network_modes.filter(item => item.id_network === this.selected_network.id && item.id_network_mode_theme === this.selected_network_mode_theme)[0];
        }
      }
      else if (this.selected_network && this.filteredNetwokModeThemes === null) {

        current_network_mode = this.mainStore.network_modes.filter(item => item.id_network == this.selected_network.id)[0];

      }

      return current_network_mode;

    },


    async getQuestions() {

      this.questions = [];
      this.current_network_mode = this.getCurrentNetworkMode();

      if (this.current_network_mode) {
      
        this.questions = await this.getNetworkModeQuestions(this.current_network_mode.id_network_mode)
      }

    },



    async getUserTools() {

      const tools = await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/datawise/user_tools');
      this.user_tools = tools.data;
    },

    async getUserNarratives() {

      const narratives = await this.$axios.get(process.env.VUE_APP_BACKEND_URL + '/user/' + this.mainStore.logged_user.id + '/cycle/' + this.mainStore.selected_cycle + '/narratives');
      this.narratives = narratives.data;
    },



    async getData() {

      if (this.selected_network && this.selected_network.code !== 'narrative') {
        await this.getQuestions();
      } 

      if (this.selected_network && ['resource', 'educ_model'].includes(this.selected_network.code)) {

         await this.getNodes(this.current_network_mode.id_network_mode);
        
      }
     
      if (this.selected_network && this.selected_network.code === 'explora' && this.user_tools.length==0) {
          await this.getUserTools();
          this.selected_tools= this.getSavedSelectedTools();
      }
      if (this.selected_network && this.selected_network.code === 'narrative') {
        this.current_network_mode = this.getCurrentNetworkMode();
        await this.getUserNarratives();
        
      }

    },



    async createFormsDetails() {

      // console.log("entra a createFormDetails");

      if (this.mainStore.network_modes.length) {

        this.forms = [];
        // console.log(this.mainStore.network_modes);

        this.mainStore.network_modes.forEach(async network_mode => {

          let form = {};

          // console.log(network_mode);

          // if (network_mode.network.code !== "narrative") {


            form['network_mode'] = network_mode;

            form['id'] = network_mode.id_network_mode;
            form['name_es'] = this.getFormSectionName(network_mode, 'es');
            form['name_en'] = this.getFormSectionName(network_mode, 'en');

            const questions = await this.getNetworkModeQuestions(network_mode.id_network_mode);

            

            if (['resource', 'educ_model'].includes(network_mode.network.code)) {
              // const nodes= await this.getNodes(network_mode.id_network_mode);
              // form['total_items'] = nodes.length;    
              await this.getNodes(network_mode.id_network_mode);
              form['total_items'] = this.filteredNodes.length;
            }
            else if (network_mode.network.code == 'actor') {
              form['total_items'] = this.selected_actors.length > 0 ? this.selected_actors.length : 1;
            }
            else if (network_mode.network.code == 'explora') {
              const saved_tools_ids = this.getSavedToolsIds();
              form['total_items'] = saved_tools_ids.length > 0 ? saved_tools_ids.length : 1;
            }
            else if (network_mode.network.code == 'narrative') {
              
              form['total_items'] = this.narratives.length > 0 ? this.narratives.length : 1;
          }


          if (network_mode.network.code !== 'narrative') {

             const prefix = network_mode.id_network_mode + '_';

            const init_num_answers = Object.keys(this.answers).filter(item => item.startsWith(prefix)).length;

            form['answers'] = init_num_answers;
            form['total_questions'] = questions.length;

            
          }
          else {
            form['total_questions'] = 1;
            form['answers'] =  this.narratives.length;
          }
           

            //console.log(this.adjacency_input_forms);

            //this.adjacency_input_forms.forEach(item => console.log(item.id_network_mode));
            const adj_input_form = this.adjacency_input_forms.filter(item => item.id_network_mode == network_mode.id_network_mode)[0];


            // console.log(adj_input_form);
            form['id_adjacency_input_form'] = adj_input_form ? adj_input_form.id_adjacency_input_form : `${this.mainStore.selected_cycle}-${this.mainStore.logged_user.id}-${network_mode.id_network_mode}`;
            form['is_concluded'] = adj_input_form ? adj_input_form.Is_concluded : false;

            this.forms.push(form);
          // }

        });

      }

    },

    async initialize() {

      // console.log('Entra a Initialize de ActiveSource');

      if (this.mainStore.selected_cycle) {
        //  console.log('Entra al IF de  Initialize de ActiveSource');
        await this.getActors();
        await this.mainStore.getNetworkModes(this.mainStore.selected_cycle);
        await this.getUserResponses();
        await this.createFormsDetails();
        await this.getUserNarratives();

      }


    }
  }


}
</script>

<style>
  .v-data-table-header,
  .theme--light.v-data-table.v-data-table--fixed-header thead th  {
    background: #2196f3 !important;
  }

  .v-data-table {
    overflow-x: auto;
  }

  /* .flex-table {
    display: flex;
    flex-grow: 1;
    width: 100%;
  } */
</style>

