export var numbersFormatMixin = {

    data: () => ({

        persistentHint:true,
        percentPrecision:1,
        percentSeparator: { decimalSeparator:',' },

        integerOptions:{
                        locale: "es-CO",
                        prefix: "",
                        suffix: "",
                        length: 10,
                        precision: 0
        },

        currencyOptions:{
                        locale: "es-CO",
                        prefix: "$",
                        suffix: "",
                        length: 20,
                        precision: 0
                    },

        percentOptions:{
                        locale: "es-CO",
                        prefix: "",
                        suffix: "%",
                        length: 3,
                        precision: 0,
                        valueWhenIsEmpty:0,
                        min:0,
                        max:100                 
                    },
       
      }),


}
