import Vue from 'vue';
import VueI18n from 'vue-i18n';
import {en,es} from 'vuetify/lib/locale';


Vue.use(VueI18n)


function loadVuetifyLocales(messages){

  messages['en']['$vuetify']= en;
  messages['es']['$vuetify']= es;


  //console.log(messages);

  return messages;

}

function loadLocaleMessages () {
  const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
  //console.log(locales.keys())
  let messages = {}
  locales.keys().forEach(key => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i)
  //  console.log(matched);
    if (matched && matched.length > 1) {
      const locale = matched[1]
  //    console.log(locales(key))
      messages[locale] = locales(key)
    }
  });

  messages=loadVuetifyLocales(messages);

  //console.log(messages);

  return messages
}

export const i18n = new VueI18n({
  locale: process.env.VUE_APP_I18N_LOCALE || 'en',
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages()
})
