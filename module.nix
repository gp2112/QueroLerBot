{ config, lib, pkgs, ... }:

with lib;
let
  cfg = config.services.querolerbot;
  settingsFormat = pkgs.formats.toml {};
in {

  options.services.querolerbot = {
    enable = mkEnableOption "querolerbot service";

    package = mkOption {
      type = types.package;
      default = pkgs.querolerbot;
    };

    user = mkOption {
      type = types.str;
      default = "querolerbot";
    };

    home = mkOption {
      type = types.str;
      default = "/var/querolerbot/";
    };

    configFile = mkOption {
      type = types.str;
      default = "/etc/querolerbot.toml";
    };

    credentials = mkOption {
      type = types.submodule {
        options = {
          accessKey = mkOption {
            type = types.str;
          };
          accessSecret = mkOption {
            type = types.str;
          };
          consumerKey = mkOption {
            type = types.str;
          };
          consumerSecret = mkOption {
            type = types.str;
          };
          token = mkOption {
            type = types.str;
          };

        };
      };
    };

    settings = mkOption {
      type = settingsFormat.type;
      default = {};
    };
  };

  config = mkIf cfg.enable {
    services.querolerbot.settings = {
      general.delay = mkDefault 15;

      twitter = {
        username = mkDefault "querolerbot";
        api_url = mkDefault "https://api.twitter.com/";
      };
      telegraph = {
        username = mkDefault "@querolerbot";
        url = mkDefault "https://graph.org/";
      };
      messages = {
        success = mkDefault [
          "Aqui está seu artigo sem paywall :)"
          "Bip, bop"
          "Saindo do forno ;)"
          "Tá sentindo? Cherinho de artigo sem paywall <3"
          "Ahoy"
          "Hello There..."
        ];
        error = {
          url_not_found = mkDefault "Não achei nenhum link :(";
          text_not_found = mkDefault "Infelizmente não consegui encontrar o texto ou o site ainda não é suportado :(\nVeja os sites compatíveis no meu perfil :)";
        };
      };
      database = {
        name = mkDefault "articles.db";
      };
    };

    environment.etc."querolerbot.toml".source =
      settingsFormat.generate "config.toml" cfg.settings;

    users.users.${cfg.user} = {
      inherit (cfg) home;
      isSystemUser = true;
      group = cfg.user;
      createHome = true;
    };

    users.groups.${cfg.user} = {};

    systemd.services.querolerbot = {
      description = "QueroLerBot";
      wantedBy = [ "multi-user.target" ];
      environment = {
        QUEROLER_CONFIG_PATH = "/etc/querolerbot.toml";
      };
      serviceConfig = {
        ExecStart = "${cfg.package}/bin/querolerbot";
        Restart = "on-failure";
        User = cfg.user;
      };
      reloadIfChanged = true;
    };
  };
}
