<template>
  <div>
    <v-text-field
      v-model="cmpValue"
      v-bind:label="label"
      v-bind:placeholder="placeholder"
      v-bind:readonly="readonly"
      v-bind:disabled="disabled"
      v-bind:outlined="outlined"
      v-bind:dense="dense"
      v-bind:hide-details="hideDetails"
      v-bind:error="error"
      v-bind:error-messages="errorMessages"
      v-bind:rules="rules"
      v-bind:clearable="clearable"
      v-bind:backgroundColor="backgroundColor"
      v-bind:prefix="options.prefix"
      v-bind:suffix="options.suffix"
      v-bind:hint="hint"
      v-bind:persistent-hint="persistentHint"
      v-bind="properties"
      v-bind:solo="solo"

      v-on:keypress="keyPress"
      v-on:blur="onBlur"
      
      
      
    ></v-text-field>
  </div>
</template>

<script>
export default {
 
  model: { prop: "value", event: "input" },
  props: {

    value: {
      // type: String,
      type: [String, Number],
      default: "0"
    },
    label: {
      type: String,
      default: ""
    },
    placeholder: {
      type: String,
      default: undefined
    },
    readonly: {
      type: Boolean,
      default: false
    },
    dense: {
      type: Boolean,
      default: false
    },
    error: {
      type: Boolean,
      default: false
    },
    hideDetails: {
      type: [Boolean, String],
      default: false
    },
    errorMessages: {
      type: [Array, String],
      default: () => []
    },
    rules: {
      type: [Array, String],
      default: () => []
    },
    hint: {
      type: String,
      default: ""
    },
    persistentHint: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    outlined: {
      type: Boolean,
      default: false
    },
    clearable: {
      type: Boolean,
      default: false
    },
    backgroundColor: {
      type: String,
      default: "white"
    },
    valueWhenIsEmpty: {
      type: String,
      default: "" // "0" or "" or null
    },
    valueOptions: {
      type: Object,
      default: function() {
        return {
          min: 0,
          minEvent: "SetValueMin"
        };
      }
    },
    options: {
      type: Object,
      default: function() {
        return {
          locale: "pt-BR",
          prefix: "",
          suffix: "",
          length: 11,
          precision: 2
        };
      }
    },
    // Other v-text-field properties
    properties: {
      type: Object,
      default: function() {
        return {};
      }
    },
    solo: {
      type: Boolean,
      default: false
    },
  },
  data: () => ({

    //errorMessages:[]

  }),
  /*
   v-model="cmpValue": Dessa forma, ao digitar, o valor é atualizado automaticamente no componente pai.
   O valor digitado entra pelo newValue do Set e é emitido para o componente pai.
   the-vue-mask nao funciona corretamente ao incluir valores existentes no componente pai.
  */
  computed: {


    cmpValue: {
      get: function() {

        // console.log('get cmpValue');
        // console.log(this.value.toString());
        return (this.value !== null && this.value !== "") ? this.humanFormat(this.value.toString()) : this.valueWhenIsEmpty;
      },
      set: function(newValue) {
        // console.log('set New value');
        // console.log(newValue);

        this.$emit("input", this.machineFormat(newValue));
      }
    }


  },
  methods: {


    humanFormat: function(number) {
      // console.log('humanFormat');
      // console.log(number);
      if (isNaN(number)) {
        number = "";
      } else {
        // number = Number(number).toLocaleString(this.options.locale, {maximumFractionDigits: 2, minimumFractionDigits: 2, style: 'currency', currency: 'BRL'});
        number = Number(number).toLocaleString(this.options.locale, {
          maximumFractionDigits: this.options.precision,
          minimumFractionDigits: this.options.precision
        });
      }
      return number;
    },


     // Incluir ponto na casa correta, conforme a precisão configurada
    addsDecimalSeparator(number){

        if(this.options.precision>0){

          const distance = number.length - parseInt(this.options.precision);
          number =number.substring(0,distance) + "." + number.substring(distance,number.length);

        }

        return number;


    },


    machineFormat(number) {

      //  console.log('machineFormat 1');
      //  console.log(number);
      if (number) {
          number = this.cleanNumber(number);

          // console.log('despues de cleanNumber');
          // console.log(number);
          // Ajustar quantidade de zeros à esquerda
          number = number.padStart(parseInt(this.options.precision) + 1, "0");

          // console.log('despues de adStart');
          // console.log(number);


          number = this.addsDecimalSeparator(number);

          // console.log('machineFormat 3');
          // console.log(number);

          if (isNaN(number)) {
            number = this.valueWhenIsEmpty;
          }

          // if(this.hitMaxLimit(number)){

          //   number = this.options.max.toString();
          //   number = number.padEnd(parseInt(this.options.length), "0");
          //   number = this.addsDecimalSeparator(number);

          // }
          // else{
          //   this.errorMessages.pop();

          // }
      }
      else {
          number = this.valueWhenIsEmpty;
      }
      // console.log('machineFormat 4');
      // console.log(number);
      
      if (this.options.precision === 0) {
        number = this.cleanNumber(number);
      }

      // console.log('machineFormat 5');
      // console.log(number);


      return number;
    },


    keyPress($event) {
      // console.log('$event.keyCode'); 
      // console.log($event.keyCode); 

      // console.log('$event.which'); 
      // console.log($event); 

      let keyCode = $event.keyCode ? $event.keyCode : $event.which;
      // if ((keyCode < 48 || keyCode > 57) && keyCode !== 46) {
      if (keyCode < 48 || keyCode > 57) {
        // 46 is dot
          $event.preventDefault();
      }
      if (this.hitTargetLength()) {
          $event.preventDefault();
      }


    },

    // Retira todos os caracteres não numéricos e zeros à esquerda
    cleanNumber: function(value) {
      // console.log('cleanNumber');
      // console.log(value);
      
      let result = "";
      if (value) {
        // este FLAG es importante !! OJO
        let flag = false; 
        let arrayValue = value.toString().split("");

        // console.log('cleanNumber arrayValue');
        // console.log(arrayValue);

        for (var i = 0; i < arrayValue.length; i++) {
          if (this.isInteger(arrayValue[i])) {
            if (!flag) {
              // Retirar zeros à esquerda
              if (arrayValue[i] !== "0") {
                result = result + arrayValue[i];
                flag = true;
              }
            } else {
              result = result + arrayValue[i];
            }
          }
        }
      }
     
      if(result=="") {
        result="0";
      }

      // console.log('en cleanNumber=');
      // console.log(result);
      return result;
    },


    isInteger(value) {
     
      return (Number.isInteger(parseInt(value))) ;
    },


    hitTargetLength() {

      // console.log(this.value);
      // console.log(this.cleanNumber(this.value));
      // console.log(Number(this.cleanNumber(this.value)));
      // console.log(Number(this.options.max));

      return (Number(this.cleanNumber(this.value).length) >= Number(this.options.length));
    },

    hitMaxLimit(number){

      // console.log(this.cleanNumber(this.value));
      // console.log(Number(this.cleanNumber(this.value)));
      // console.log(Number(this.options.max));

  
      return (this.options.max && Number(number) > Number(this.options.max));


    },


    onBlur() {
      // console.log('onBlur');
      // console.log(this.value);
      // console.log(this.value.length);

      if ((this.value && this.value.length === 0) || (parseFloat(this.value) <= this.valueOptions.min)){

          this.$emit(
          this.valueOptions.minEvent || "SetValueMin",
          this.valueOptions.min
        );

        
      }

    
      if (this.valueOptions.max && parseFloat(this.value) >= this.valueOptions.max){

          this.$emit(
          this.valueOptions.maxEvent || "SetValueMax",
          this.valueOptions.max
        );
      }

      
    }
  }
};
</script>
