import React, { useEffect, useState } from 'react'

import { Alert, Container, Button, Form, Table } from 'react-bootstrap'

import axios from 'axios'

const Urlcounts = () => {
    const [error, setError] = useState<string>('')
    const [submitting, setSubmitting] = useState(false)
    const [submitSuccess, setSubmitSuccess] = useState(false)
    const [urlsValue, setUrlsValue] = useState<string>('')
    const [resultJSON, setResultJSON] = useState<any>({})

    const onClear = () => {
        // Reset states.
        setError('')
        setSubmitSuccess(false)
        setUrlsValue('')
        setResultJSON({})
    }

    const onSubmit = () => {
        // Reset states.
        setError('')
        setSubmitSuccess(false)

        try {
            if (urlsValue) {
                // Convert the provided URLs to JSON.
                const parsedList = urlsValue.split('\n')
                const jsonValue = {"urls": parsedList}

                // Call API for urlcounts processing.
                const settings = { headers: { Accept: 'application/json', 'Content-Type': 'application/json' } }
                setSubmitting(true)
                axios.post("http://127.0.0.1:5000/urlcounts", jsonValue, settings)
                    .then(r => {
                        setSubmitting(false)
                        setSubmitSuccess(true)
                        setResultJSON(r.data)
                    })
                    .catch(e => {
                        setSubmitting(false)
                        setError(`${e.response.status} ${e.response.data}`)
                    })
            } else {
                // Show message to <Alert> component if textarea is blank.
                setError('Please provide URLs for processing.')
            }
        } catch (e) {
            // Show error message to <Alert> component.
            setError((e as Error).message)
        }
    }

    // Page rendering.
    return (
        <Container className="mt-3 mb-3">
            <h2 className="mb-3">Corsearch Technical Challenge - Urlcounts <small>(by Anson Lam)</small></h2>

            <Form>
                {/* URLs textbox. */}
                <Form.Group className="mb-3">
                    <Form.Label>Please paste URLs into the textbox below and click Submit:</Form.Label>
                    <Form.Control
                        as="textarea"
                        value={urlsValue}
                        onChange={e => setUrlsValue(e.target.value)}
                        rows={8}
                        disabled={submitting}
                    />
                </Form.Group>

                {/* Submit button. */}
                <Button onClick={onSubmit} disabled={submitting}>
                    Submit
                </Button>

                {/* Clear button. */}
                &nbsp;
                <Button onClick={onClear} disabled={submitting}>
                    Clear
                </Button>

                {/* Alert error message. */}
                {error &&
                    <Alert variant='danger' className="mt-3">{error}</Alert>
                }
                {/* Alert success message. */}
                {submitSuccess &&
                    <Alert variant='success' className="mt-3">URLs processed successfully.</Alert>
                }

                {/* Urlcounts result. */}
                {submitSuccess &&
                    <div className="mt-5">
                        <h4 className="mb-3">Urlcounts Result:</h4>

                        <Form.Label>
                            The count of URLs that did match a host : <b>{resultJSON?.count_urls_match_a_host}</b>
                        </Form.Label><br/>

                        <Form.Label>
                            The count of URLs that did not match any hosts :&nbsp;
                            <b>{resultJSON?.count_urls_not_match_any_hosts}</b>
                        </Form.Label><br/>

                        <Form.Group>
                            <Form.Label>
                                A list of all unique hosts for which there was a matching URL with a count of URLs that matched :
                            </Form.Label>
                            <Form.Control as="textarea" rows={8}
                                value={resultJSON?.count_urls_matched_per_host.join('\n')}
                                disabled readOnly
                            />
                        </Form.Group>

                        <Form.Group className="mt-2">
                            <Form.Label>A list of all URLs that did not match any hosts :</Form.Label>
                            <Form.Control as="textarea" rows={8}
                                value={resultJSON?.urls_not_match_any_hosts.join('\n')}
                                disabled readOnly
                            />
                        </Form.Group>
                    </div>
                }
            </Form>
        </Container>
    )
}

export default Urlcounts
