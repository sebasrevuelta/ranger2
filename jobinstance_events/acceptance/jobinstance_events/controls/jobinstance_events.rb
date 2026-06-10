# frozen_string_literal: true

control 'jobinstance-events-service' do
  title 'jobinstance_events service acceptance checks'
  desc 'Validate that the service image exposes the expected HTTP health endpoint.'

  describe http('http://localhost:8080/healthz') do
    its('status') { should cmp 200 }
    its('body') { should match(/ok/) }
  end

  describe http('http://localhost:8080/readyz') do
    its('status') { should cmp 200 }
  end
end
