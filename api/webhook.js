export default async function handler(req, res) {
  // Handle Instagram webhook verification (GET request)
  if (req.method === 'GET') {
    const verifyToken = process.env.WEBHOOK_VERIFY_TOKEN || 'instagram_webhook_secret_2024';
    const hubVerifyToken = req.query['hub.verify_token'];
    const hubChallenge = req.query['hub.challenge'];
    
    if (hubVerifyToken === verifyToken) {
      console.log('✅ Webhook verified successfully');
      return res.status(200).send(hubChallenge);
    } else {
      console.log('❌ Webhook verification failed');
      return res.status(403).send('Forbidden');
    }
  }
  
  // Handle Instagram webhook events (POST request)
  if (req.method === 'POST') {
    try {
      const body = req.body;
      console.log('📱 Received Instagram webhook:', JSON.stringify(body, null, 2));
      
      // Check if this is a comment event
      let hasCommentEvent = false;
      
      for (const entry of body.entry || []) {
        for (const change of entry.changes || []) {
          if (change.field === 'comments') {
            hasCommentEvent = true;
            const commentData = change.value;
            const commentText = commentData.text?.trim().toUpperCase();
            
            console.log(`📝 Comment received: "${commentText}"`);
            
            // Check if comment matches our trigger
            if (commentText === 'FUN FACT') {
              console.log('🎯 FUN FACT trigger detected! Triggering GitHub Action...');
              
              // Trigger GitHub Action via Repository Dispatch
              const githubResponse = await fetch('https://api.github.com/repos/domenecmiralles/scheduled_posting/dispatches', {
                method: 'POST',
                headers: {
                  'Authorization': `token ${process.env.GITHUB_TOKEN}`,
                  'Accept': 'application/vnd.github.v3+json',
                  'Content-Type': 'application/json',
                  'User-Agent': 'Instagram-Webhook-Handler'
                },
                body: JSON.stringify({
                  event_type: 'instagram_fun_fact_comment',
                  client_payload: {
                    comment_id: commentData.id,
                    user_id: commentData.from?.id,
                    media_id: commentData.media?.id,
                    comment_text: commentData.text,
                    timestamp: new Date().toISOString()
                  }
                })
              });
              
              if (githubResponse.ok) {
                console.log('✅ GitHub Action triggered successfully');
              } else {
                console.log('❌ Failed to trigger GitHub Action:', await githubResponse.text());
              }
            }
          }
        }
      }
      
      if (!hasCommentEvent) {
        console.log('ℹ️ No comment events in webhook');
      }
      
      return res.status(200).json({ status: 'success', message: 'Webhook processed' });
      
    } catch (error) {
      console.error('❌ Error processing webhook:', error);
      return res.status(500).json({ status: 'error', message: error.message });
    }
  }
  
  // Method not allowed
  return res.status(405).json({ status: 'error', message: 'Method not allowed' });
}
