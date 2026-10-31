from apps.api.app import config

def test_local_env_credentials_override_unrelated_parent_shell(monkeypatch,tmp_path):
 env=tmp_path/'demo.env';env.write_text('ANTHROPIC_API_KEY=file-demo-key\nPCC_TEST_FLAG=file\n')
 monkeypatch.setattr(config,'ENV',env);monkeypatch.setattr(config,'SERVERLESS',False)
 monkeypatch.setenv('ANTHROPIC_API_KEY','parent-demo-key');monkeypatch.setenv('PCC_TEST_FLAG','operator')
 assert config.get('ANTHROPIC_API_KEY')=='file-demo-key'
 assert config.get('PCC_TEST_FLAG')=='operator'

def test_hosted_settings_use_runtime_environment_without_local_file(monkeypatch,tmp_path):
 env=tmp_path/'absent.env';monkeypatch.setattr(config,'ENV',env);monkeypatch.setattr(config,'SERVERLESS',True)
 monkeypatch.setenv('ANTHROPIC_API_KEY','hosted-demo-key')
 assert config.get('ANTHROPIC_API_KEY')=='hosted-demo-key' and not env.exists()
