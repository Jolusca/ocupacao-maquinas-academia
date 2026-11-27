#include <Arduino.h>
#include <Preferences.h>
#include "node_config.h"

static const char *NAMESPACE = "no";
static const char *KEY_ID = "id";
static const char *KEY_MODE = "modo";

uint8_t node_cfg_id()
{
    Preferences prefs;
    uint8_t id;

    prefs.begin(NAMESPACE, true);
    id = prefs.getUChar(KEY_ID, 0);
    prefs.end();
    return id;
}

role_mode_t node_cfg_mode()
{
    Preferences prefs;
    uint8_t mode;

    prefs.begin(NAMESPACE, true);
    mode = prefs.getUChar(KEY_MODE, (uint8_t)ROLE_MODE_AUTO);
    prefs.end();
    /* Valor estranho na flash: volta ao automático em vez de adivinhar. */
    if (mode > (uint8_t)ROLE_MODE_SENSOR)
    {
        return ROLE_MODE_AUTO;
    }
    return (role_mode_t)mode;
}

void node_cfg_save_id(uint8_t id)
{
    Preferences prefs;

    prefs.begin(NAMESPACE, false);
    prefs.putUChar(KEY_ID, id);
    prefs.end();
}

void node_cfg_save_mode(role_mode_t mode)
{
    Preferences prefs;

    prefs.begin(NAMESPACE, false);
    prefs.putUChar(KEY_MODE, (uint8_t)mode);
    prefs.end();
}

void node_cfg_clear()
{
    Preferences prefs;

    prefs.begin(NAMESPACE, false);
    prefs.clear();
    prefs.end();
}
